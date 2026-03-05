import os
import io
import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from typing import List, Dict, Any

# Configuration
CREDENTIALS_FILE = "/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json"
FOLDER_ID = "1-Oa71omBAXEWmMqRchkrC7c6T0fdeySP"
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
DOWNLOAD_DIR = "uploads" # Sync to the same uploads dir used by the API

def get_drive_service():
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"Credentials file not found at {CREDENTIALS_FILE}")
    
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def list_files(service, folder_id):
    results = []
    page_token = None
    while True:
        try:
            # Query for files in the folder and not trashed
            q = f"'{folder_id}' in parents and trashed = false"
            response = service.files().list(
                q=q,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, size)',
                pageToken=page_token
            ).execute()
            
            items = response.get('files', [])
            results.extend(items)
            
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return results

def download_file(service, file_id, file_name, destination_folder):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    
    print(f"Downloading {file_name}...")
    try:
        while done is False:
            status, done = downloader.next_chunk()
        
        # Save to disk
        filepath = os.path.join(destination_folder, file_name)
        with open(filepath, "wb") as f:
            f.write(fh.getbuffer())
        print(f"Saved to {filepath}")
        return filepath
    except Exception as e:
        print(f"Failed to download {file_name}: {e}")
        return None

def sync_folder(service, folder_id, local_path):
    os.makedirs(local_path, exist_ok=True)
    files = list_files(service, folder_id)
    
    for file in files:
        file_name = file['name']
        mime_type = file.get('mimeType', '')
        
        if mime_type == 'application/vnd.google-apps.folder':
            print(f"Directory: {file_name}")
            new_local_path = os.path.join(local_path, file_name)
            sync_folder(service, file['id'], new_local_path)
            
        elif 'application/vnd.google-apps' in mime_type:
             print(f"Skipping Google native format: {file_name}")
             
        else:
             download_file(service, file['id'], file_name, local_path)

def main():
    print(f"Authenticating with {CREDENTIALS_FILE}...")
    try:
        service = get_drive_service()
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    print(f"Starting recursive sync from folder {FOLDER_ID}...")
    sync_folder(service, FOLDER_ID, DOWNLOAD_DIR)


if __name__ == '__main__':
    main()
