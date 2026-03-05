import sys
import os
import json
import time
import concurrent.futures
from google.cloud import storage
from google.cloud import bigquery
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Derive absolute paths from this script's location
# Script lives at: HiveMind/src/extractor/fast_backfill.py
# Repo root is:    HiveMind/../../ (i.e., /Users/timstevens/Antigravity)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_HIVEMIND_ROOT = os.path.dirname(os.path.dirname(_SCRIPT_DIR))  # HiveMind/
_REPO_ROOT = os.path.dirname(_HIVEMIND_ROOT)  # Antigravity/

# Configuration
PROJECT_ID = 'augos-core-data'
BUCKET_NAME = 'augos-core-data-raw-email-lake'
DATASET_ID = 'hive_mind_core'
TABLE_ID = 'staging_raw_emails'

SERVICE_ACCOUNT_FILE = os.path.join(_HIVEMIND_ROOT, 'credentials', 'hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

# Add repository root to path for imports
sys.path.insert(0, _REPO_ROOT)
from HiveMind.src.admin.list_all_users import list_domain_users

TARGET_USERS = list_domain_users()
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.labels']

# Clients (Thread-safe-ish, but usually better to let library handle)
bq_client = bigquery.Client()
storage_client = storage.Client()

def get_gmail_service(user_email):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    creds = creds.with_subject(user_email)
    return build('gmail', 'v1', credentials=creds, cache_discovery=False)

def process_single_email(gmail_service, msg_summary, user_email):
    """
    Fetches full content, uploads to GCS, returns metadata for BQ.
    Executed in a thread.
    """
    msg_id = msg_summary['id']
    thread_id = msg_summary['threadId']

    try:
        # 1. Fetch Full Content
        full_msg = gmail_service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        
        # 2. Upload to GCS
        bucket = storage_client.bucket(BUCKET_NAME)
        blob_name = f"raw/{time.strftime('%Y/%m/%d')}/{msg_id}.json"
        blob = bucket.blob(blob_name)
        blob.upload_from_string(json.dumps(full_msg), content_type='application/json')

        # 3. Extract Metadata
        headers = full_msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        recipient = next((h['value'] for h in headers if h['name'] == 'Delivered-To'), None)
        if not recipient:
            recipient = next((h['value'] for h in headers if h['name'] == 'To'), 'Unknown')
            
        snippet = full_msg.get('snippet', '')
        timestamp = float(full_msg.get('internalDate', 0)) / 1000.0

        # Return Row for Bundle
        return {
            "message_id": msg_id,
            "thread_id": thread_id,
            "timestamp": timestamp, 
            "sender": sender,
            "recipient": recipient if recipient else user_email, # Fallback to owner
            "subject": subject,
            "snippet": snippet,
            "raw_gcs_uri": f"gs://{BUCKET_NAME}/{blob_name}",
            "processing_status": "PENDING"
        }

    except Exception as e:
        print(f"  ❌ Error processing {msg_id}: {e}")
        return None

def run_fast_backfill(start_date="2026/01/20"):
    print(f"🚀 Starting FAST Backfill (ThreadPool) from {start_date}...")
    
    # We need a separate service instance per thread? 
    # Actually, googleapiclient is NOT thread safe.
    # Approach: Create a pool of services or reuse one with caution. 
    # Safest: One service passed to thread, but that blocks parallel calls if it locks.
    # Better: Use `http` object per thread.
    # Simplest for script: Just instantiate service inside thread? Expensive.
    # Compromise: Instantiate 1 service per worker in an initializer?
    # Or just rely on the fact that `build()` creates a resource that MIGHT be thread safe if used carefully?
    # Documentation says: "The client library is not thread-safe."
    # OK, we will create a lightweight wrapper content.
    
    for user_email in TARGET_USERS:
        print(f"\n🔵 Processing User: {user_email}")
        
        # Master service for listing
        master_service = get_gmail_service(user_email)
        query = f"after:{start_date}"
        page_token = None
        total_processed = 0
        
        while True:
            try:
                # 1. List Batch (200 items)
                results = master_service.users().messages().list(
                    userId='me', q=query, pageToken=page_token, maxResults=200
                ).execute()
                
                messages = results.get('messages', [])
                if not messages:
                    break
                    
                print(f"  Batch: Found {len(messages)} messages. Spawning threads...")
                
                bq_rows = []
                
                # 2. Parallel Fetch & Upload
                # We need fresh services for threads to be safe
                # This construct passes a fresh service to each call is too slow.
                # Actually, many people share the service. Let's try sharing. 
                # If it fails, we make it robust.
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    # We create a local service for each submission? No, that's 200 auth calls.
                    # Let's try sharing `master_service`. If it crashes, we switch strategies.
                    # Update: `httplib2` used by `google-api-python-client` is not thread safe.
                    # We MUST Create a new service object, OR duplicate the http object.
                    # Optimization: create N services (N=20) and cycle them? 
                    # Let's try simply creating a new service inside the function for now. 
                    # It's an auth call but might be fast enough compared to the 3 HTTP calls it saves.
                    
                    params = [(messages[i], user_email) for i in range(len(messages))]
                    
                    # We need a helper that creates its own service
                    futures = [executor.submit(process_wrapper, p) for p in params]
                    
                    for future in concurrent.futures.as_completed(futures):
                        row = future.result()
                        if row:
                            bq_rows.append(row)
                            
                # 3. Batch Insert to BigQuery
                if bq_rows:
                    errors = bq_client.insert_rows_json(f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}", bq_rows)
                    if errors:
                        print(f"  ⚠️ BQ Errors: {errors}")
                    else:
                        total_processed += len(bq_rows)
                        print(f"  ✅ Batch Committed. Total for user: {total_processed}")

                page_token = results.get('nextPageToken')
                if not page_token:
                    break
                    
            except Exception as e:
                print(f"Critial Loop Error: {e}")
                break

def process_wrapper(args):
    msg, user_email = args
    # Per-thread service instantiation for safety
    service = get_gmail_service(user_email)
    return process_single_email(service, msg, user_email)

if __name__ == '__main__':
    run_fast_backfill()
