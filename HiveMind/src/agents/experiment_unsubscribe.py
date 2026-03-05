import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

# Setup similar to backfill.py
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
# We need to impersonate Tim to see his mail
from google.oauth2 import service_account

def get_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    creds = creds.with_subject('tim@augos.io')
    return build('gmail', 'v1', credentials=creds)

def check_headers():
    service = get_service()
    
    # specific sender we saw earlier
    query = "from:fool@info.fool.com" 
    
    results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found from Motley Fool.")
        return

    msg_id = messages[0]['id']
    msg = service.users().messages().get(userId='me', id=msg_id, format='metadata').execute()
    
    headers = msg['payload']['headers']
    
    print(f"Checking Message: {msg_id}")
    for h in headers:
        if h['name'].lower() in ['list-unsubscribe', 'list-unsubscribe-post']:
            print(f"{h['name']}: {h['value']}")

if __name__ == '__main__':
    check_headers()
