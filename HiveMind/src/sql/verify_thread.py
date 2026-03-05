from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import base64

# Env Config
PROJECT_ID = 'augos-core-data'
# NOTE: Using same credentials, but in Python we need to replicate the DWD logic.
SERVICE_ACCOUNT_FILE = os.path.abspath('credentials/hive-mind-admin.json')

def verify_thread_fetch():
    print("Verifying Gmail Thread Fetch (Python DWD)...\n")
    
    # 1. Auth with DWD
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, 
        scopes=['https://www.googleapis.com/auth/gmail.readonly'],
        subject='tim@augos.io'
    )
    
    service = build('gmail', 'v1', credentials=creds)

    # 2. List one thread to get an ID
    results = service.users().threads().list(userId='me', maxResults=1).execute()
    threads = results.get('threads', [])
    
    if not threads:
        print("No threads found in inbox.")
        return

    thread_id = threads[0]['id']
    print(f"Fetching Thread ID: {thread_id}")

    # 3. Get Full Thread
    thread = service.users().threads().get(userId='me', id=thread_id, format='full').execute()
    
    print(f"Thread Retrieved with {len(thread.get('messages', []))} messages.")
    
    for msg in thread.get('messages', []):
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        snippet = msg.get('snippet', '')
        print(f" - [{msg['id']}] {subject[:40]}... : {snippet[:50]}...")

if __name__ == "__main__":
    verify_thread_fetch()
