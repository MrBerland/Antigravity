import sys
import os

# Configuration (MUST BE SET BEFORE IMPORTING main)
os.environ['PROJECT_ID'] = 'augos-core-data'
os.environ['BUCKET_NAME'] = 'augos-core-data-raw-email-lake'
os.environ['DATASET_ID'] = 'hive_mind_core'
os.environ['TABLE_ID'] = 'messages'

# Hack: Add current directory to path so we can import 'main'
sys.path.append(os.path.join(os.getcwd(), 'HiveMind/src/extractor'))

# Import the core logic from our Cloud Function code
from main import process_message_id

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
# CRITICAL: Set ADC for BigQuery, Storage, and Vertex AI to use this key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE


TARGET_USERS = [
    'tim@augos.io',
    'maretha@augos.io',
    'chris@augos.io',
]
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.labels']

def get_gmail_service(user_email=None):
    """Authenticates as Service Account impersonating TARGET_USER."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    if user_email:
        creds = creds.with_subject(user_email)
    return build('gmail', 'v1', credentials=creds)

def run_backfill(start_date="2024/01/01"):
    print(f"🚀 Starting Hive Mind Multi-User Backfill from {start_date}...")
    
    for user_email in TARGET_USERS:
        print(f"\n🔵 Processing User: {user_email}")
        try:
            service = get_gmail_service(user_email)
            query = f"after:{start_date}"
            
            # Pagination Loop
            page_token = None
            processed_count = 0
            
            while True:
                try:
                    results = service.users().messages().list(
                        userId='me', 
                        q=query, 
                        pageToken=page_token,
                        maxResults=200 # Bumped up
                    ).execute()
                    
                    messages = results.get('messages', [])
                    
                    if not messages:
                        print(f"  No messages found for {user_email}.")
                        break
                        
                    print(f"  Batch: Found {len(messages)} messages. Processing...")
                    
                    for msg in messages:
                        try:
                            msg_id = msg['id']
                            # Call the Updated main.py logic (pass service to avoid re-auth)
                            process_message_id(msg_id, gmail_service=service, user_email=user_email)
                            processed_count += 1
                            
                            if processed_count % 20 == 0:
                                print(f"  Progress: {processed_count} emails so far...")
                                
                        except Exception as e:
                            print(f"  ❌ Error processing {msg_id}: {e}")
            
                    page_token = results.get('nextPageToken')
                    if not page_token:
                        break
                        
                except Exception as e:
                    print(f"  Critical Error in Batch Loop: {e}")
                    break
                    
            print(f"✅ User {user_email} Complete. Processed: {processed_count}")
            
        except Exception as e:
            print(f"❌ Failed to init service for {user_email}: {e}")

    print("\n🏁 Full Backfill Complete.")

if __name__ == '__main__':
    run_backfill()
