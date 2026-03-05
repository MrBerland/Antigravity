import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
# We need to impersonate an admin to list users
ADMIN_EMAIL = 'tim@augos.io' 
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user.readonly']

def list_domain_users():
    # Admin SDK Scope failed (Unauthorized Client). 
    # Fallback to hardcoded list discovered from previous diagnostics.
    # Ideally, we would use the Admin SDK if the Service Account had Domain-Wide Delegation for that scope.
    
    known_users = [
        'tim@augos.io',
        'maretha@augos.io',
        'chris@augos.io',
        'oliver@augos.io',
        'support@augos.io',
        'tim+canned.response@augos.io'
    ]
    
    # Try to load from config file if exists
    config_path = os.path.abspath('HiveMind/config/users_list.json')
    if os.path.exists(config_path):
        import json
        with open(config_path, 'r') as f:
            file_users = json.load(f)
            if isinstance(file_users, list):
                print(f"Loaded {len(file_users)} users from config file.")
                return file_users

    print(f"Using known user list ({len(known_users)} users)")
    return known_users

if __name__ == "__main__":
    list_domain_users()
