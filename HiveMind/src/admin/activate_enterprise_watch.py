import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
# Path to your Service Account JSON key
SERVICE_ACCOUNT_FILE = 'HiveMind/credentials/hive-mind-admin.json'

# The user to impersonate (admin or specific user)
# Ideally, you iterate through a list of users here.
# For this script, we'll start with the current user or a list.
TARGET_USERS = [
    'tim@augos.io' 
    # Add more users here, or fetch from Directory API if you add the scope
]

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
PROJECT_ID = "augos-core-data"
TOPIC_NAME = f"projects/{PROJECT_ID}/topics/gmail-ingest-topic"

def get_gmail_service(user_email):
    """
    Authenticates as the Service Account but IMPERSONATING the given user.
    """
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    delegated_creds = creds.with_subject(user_email)
    return build('gmail', 'v1', credentials=delegated_creds)

def activate_watch_for_user(user_email):
    print(f"🔌 Activating Hive Mind for: {user_email}...")
    
    try:
        service = get_gmail_service(user_email)
        
        request_body = {
            'labelIds': ['INBOX'], 
            'topicName': TOPIC_NAME,
            'labelFilterAction': 'include'
        }
        
        response = service.users().watch(userId='me', body=request_body).execute()
        
        print(f"✅ [SUCCESS] {user_email} is now being watched.")
        print(f"   History ID: {response.get('historyId')}")
        
    except Exception as e:
        print(f"❌ [FAILED] {user_email}: {e}")

def main():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Error: Credential file not found at {SERVICE_ACCOUNT_FILE}")
        print("Please follow the setup guide to create the Service Account key.")
        return

    print("🚀 Starting Enterprise Activation (Domain-Wide Delegation)...")
    
    for user in TARGET_USERS:
        activate_watch_for_user(user)

if __name__ == '__main__':
    main()
