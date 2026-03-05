import base64
import json
import os
import time
from google.cloud import storage
from google.cloud import bigquery
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Environment Variables
PROJECT_ID = os.environ.get('PROJECT_ID')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
DATASET_ID = os.environ.get('DATASET_ID')
TABLE_ID = os.environ.get('TABLE_ID')

# Global lazy clients
_storage_client = None
_bq_client = None

def get_storage_client():
    global _storage_client
    if not _storage_client:
        _storage_client = storage.Client()
    return _storage_client

def get_bq_client():
    global _bq_client
    if not _bq_client:
        _bq_client = bigquery.Client()
    return _bq_client

def mark_as_ignored(service, msg_id):
    """Applies 'HiveMind-Ignored' label to the message in Gmail for user visibility."""
    try:
        # First, we need the Label ID. Ideally we'd look it up, but creating it is safer.
        # For MVP speed, let's assume we just log it, or try to apply a known ID?
        # Better: Just log for now to avoid Label ID lookup complexity in this Cloud Function, 
        # UNLESS we want to do the full create-if-not-exists dance.
        # Let's do a simple modify with a specific Label Name if it exists, logic is complex.
        # SIMPLIFICATION: User asked to "SEE" it.
        # Let's actually create the label if missing.
        user_id = 'me'
        label_name = 'HiveMind-Ignored'
        
        # 1. List labels to find ID
        results = service.users().labels().list(userId=user_id).execute()
        labels = results.get('labels', [])
        label_id = next((l['id'] for l in labels if l['name'] == label_name), None)
        
        if not label_id:
            # Create it
            created = service.users().labels().create(userId=user_id, body={'name': label_name}).execute()
            label_id = created['id']
            
        # 2. Apply Label
        service.users().messages().modify(userId=user_id, id=msg_id, body={'addLabelIds': [label_id]}).execute()
        print(f"Tagged message {msg_id} as {label_name}")
    except Exception as e:
        print(f"Warning: Could not tag ignored message: {e}")

import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

def call_ai_bouncer(email_content):
    """
    Asks Gemini: Is this email safe for the company knowledge base?
    Returns: (is_safe: bool, reason: str, category: str)
    """
    vertexai.init(project=PROJECT_ID, location="us-central1")
    
    # Try 2.0 Flash first (Smarter/Free-Preview), fallback to 1.5 Flash (Reliable/Cheap)
    model_name = "gemini-2.0-flash-exp"
    
    prompt = f"""
    You are the "Bouncer" for a corporate knowledge base (Hive Mind).
    Your job is to BLOCK sensitive HR/Private data and ALLOW business data (including chatter, tickets, alerts).

    EMAIL CONTENT:
    {email_content}

    INSTRUCTIONS:
    1. ANALYZE if the email contains:
       - Payroll, Salary, Compensation details (BLOCK)
       - Resignation, Disciplinary action, HR disputes (BLOCK)
       - Personal private medical/family issues (BLOCK)
       - Everything else (ALLOW) - e.g., "Lunch plans?", "Server is down", "Client Invoice", "Ticket #123", "Meeting notes".

    2. CATEGORIZE the email into one of:
       [OPERATIONS, SALES, SUPPORT, CHATTER, SYSTEM, HR_SENSITIVE, PERSONAL_SENSITIVE]

    3. RETURN JSON format ONLY:
       {{
         "action": "ALLOW" or "BLOCK",
         "category": "CATEGORY_NAME",
         "reason": "Short explanation"
       }}
    """
    
    try:
        model = GenerativeModel(model_name)
        response = model.generate_content(prompt)
        # Fallback if 2.0 fails or returns empty (simple retry logic implied by Architecture)
        return response.text
    except Exception as e:
        print(f"Bouncer AI Error ({model_name}): {e}")
        return None

def should_ingest(email_meta):
    """
    AI-POWERED SECURITY FILTER
    """
    labels = email_meta.get('labelIds', [])
    headers = email_meta.get('payload', {}).get('headers', [])
    snippet = email_meta.get('snippet', '')
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), '')

    # 1. Hard Block on explicit labels (Safety Net)
    blocked_labels = ['CONFIDENTIAL', 'PERSONAL', 'HIVEMIND_EXCLUDE']
    if any(b in labels for b in blocked_labels):
        return False, f"Blocked Label: {labels}"

    # 2. Prepare Context for AI
    # We use Subject + Snippet to save cost/time vs full body fetching
    email_context = f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}"
    
    # 3. Ask the AI
    ai_response_text = call_ai_bouncer(email_context)
    
    if not ai_response_text:
        # Fallback: Allow if AI fails? Or Block? 
        # For now, let's Fail Open for internal, Fail Closed for external?
        # Safer: Fail Open but Log Warning (as per "Ingest All" pivot)
        print("WARNING: Bouncer AI failed. Defaulting to ALLOW.")
        return True, "AI_FAILURE_FALLBACK"

    # Parse JSON (Simplified)
    import json
    try:
        # Clean markdown code blocks if present
        clean_json = ai_response_text.replace('```json', '').replace('```', '')
        decision = json.loads(clean_json)
        
        if decision.get('action') == 'BLOCK':
            return False, f"AI_BLOCK: {decision.get('reason')}"
        
        # TODO: We could attach the 'category' to the BigQuery insert later!
        print(f"Bouncer: AI Allowed. Category: {decision.get('category')}")
        return True, decision.get('category')
        
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return True, "JSON_PARSE_ERROR"


# REPLACEMENT FOR lines 155-240 of main.py

def get_gmail_service(user_email=None):
    """
    Returns a Gmail Service object.
    If user_email is provided, it attempts to IMPERSONATE that user (requires Domain-Wide Delegation).
    If not, it uses the default credentials (which might fail for user data if not delegated).
    """
    # In Cloud Functions, we might rely on ADC.
    # But for DWD, we often need explicit credentials + subject.
    # However, if the Service Account attached to this env var IS the DWD one, this works:
    
    # Check if we have a specific key file (Local Dev / Backfill)
    sa_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    
    scopes = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.labels']
    
    if sa_file and os.path.exists(sa_file):
        creds = service_account.Credentials.from_service_account_file(sa_file, scopes=scopes)
    else:
        # Fallback to ADC (Prod Cloud Function)
        creds, _ = google.auth.default(scopes=scopes)

    if user_email:
        # TIM STEVENS NOTE: This is the magic. 
        # The SA *must* have DWD enabled in Google Admin Console for this to work.
        # We replace the subject to "be" the user.
        # Note: ADC credentials object might differ from service_account.Credentials.
        # If this fails in Cloud Function with ADC, we might need to load the key from Secret Manager.
        # For now, assuming the local dev flow or key-based flow.
        try:
             # Basic ADC credentials don't always support with_subject directly if obtained via metadata server
             # But let's try standard path first.
             creds = creds.with_subject(user_email)
             print(f"🔑 Acting as: {user_email}")
        except AttributeError:
            print(f"⚠️ Warning: generated credentials object {type(creds)} might not support impersonation directly.")

    return build('gmail', 'v1', credentials=creds, cache_discovery=False)

def process_message_id(msg_id, gmail_service=None, user_email=None):
    """
    Core Ingestion Logic: Fetches, Filters, and Saves a single message.
    Reusable by Cloud Function (Real-time) and Backfill Script (Historical).
    Args:
        msg_id: Gmail Message ID
        gmail_service: Authenticated Gmail Resource (Optional, will create if None)
        user_email: The email of the mailbox owner (Required if creating service)
    """
    if not gmail_service:
        gmail_service = get_gmail_service(user_email)

    # --- ELT ARCHITECTURE: INGEST EVERYTHING (DUMB & FAST) ---
    # We stripped the AI Bouncer here to avoid 429 Rate Limits and Latency.
    # Logic: 1. Save Raw to GCS. 2. Insert Metadata to Staging Table. 
    # AI Processing happens asynchronously in BigQuery later.
    
    # 3. Fetch Full Content
    try:
        # userId='me' works because the service is already impersonating the right subject
        full_msg = gmail_service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    except Exception as e:
        print(f"❌ Failed to fetch message {msg_id}: {e}")
        return

    # 4. Save to GCS (Raw Lake)
    bucket = get_storage_client().bucket(BUCKET_NAME)
    blob_name = f"raw/{time.strftime('%Y/%m/%d')}/{msg_id}.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(json.dumps(full_msg), content_type='application/json')
    print(f"Uploaded raw email to gs://{BUCKET_NAME}/{blob_name}")

    # 5. Extract Metadata
    headers = full_msg['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
    # Use Delivered-To as primary recipient evidence. Fallback to To header (which can be messy).
    recipient = next((h['value'] for h in headers if h['name'] == 'Delivered-To'), None)
    if not recipient:
        recipient = next((h['value'] for h in headers if h['name'] == 'To'), 'Unknown')

    snippet = full_msg.get('snippet', '')
    thread_id = full_msg.get('threadId')
    timestamp = float(full_msg.get('internalDate', 0)) / 1000.0

    # 6. Insert into BigQuery STAGING Table
    row = [{
        "message_id": msg_id,
        "thread_id": thread_id,
        "timestamp": timestamp, 
        "sender": sender,
        "recipient": recipient, # New Column
        "subject": subject,
        "snippet": snippet,
        "raw_gcs_uri": f"gs://{BUCKET_NAME}/{blob_name}", # Renamed col
        "processing_status": "PENDING"
    }]
    
    errors = get_bq_client().insert_rows_json(f"{PROJECT_ID}.{DATASET_ID}.staging_raw_emails", row)
    if errors:
        print(f"BigQuery Staging Insert Errors: {errors}")
    else:
        print("BigQuery Staging insert success.")

def ingest_gmail_event(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic."""
    
    # 1. Decode Pub/Sub message
    if 'data' in event:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)
    else:
        print("No data in event")
        return

    email_address = message_data.get('emailAddress')
    history_id = message_data.get('historyId')
    
    print(f"Processing event for {email_address}, historyId: {history_id}")

    if not email_address:
        print("❌ Error: No emailAddress in Pub/Sub message. Cannot impersonate.")
        return

    # 2. Fetch Sync Logic (Simplified for MVP)
    # CRITICAL: Authenticate AS THIS USER
    try:
        gmail = get_gmail_service(user_email=email_address)
        
        # List one message just to test connectivity/history
        # In full production we'd use historyId to get the exact change, 
        # but for now we just check the latest message or specific logic.
        # Let's keep it simple: Just look at the latest message for the demo purpose, 
        # or rely on History API if we were robust.
        # For 'Ingest everything', fetching the latest might duplicate works. 
        # Ideally: users().history().list(startHistoryId=history_id)
        
        # MVP: Just fetch the latest 1 message to prove connection
        results = gmail.users().messages().list(userId='me', maxResults=1).execute()
        messages = results.get('messages', [])

        if not messages:
            print(f"No messages found for {email_address}.")
            return

        msg_id = messages[0]['id']
        process_message_id(msg_id, gmail_service=gmail)
        
    except Exception as e:
        print(f"❌ Failed to process event for {email_address}: {e}")

