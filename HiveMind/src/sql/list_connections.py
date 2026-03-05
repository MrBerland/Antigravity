from google.cloud import bigquery_connection_v1
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

def list_connections():
    client = bigquery_connection_v1.ConnectionServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/us"
    
    print(f"Listing connections in {parent}...")
    for connection in client.list_connections(parent=parent):
        print(f"Name: {connection.name}")
        print(f"ID: {connection.name.split('/')[-1]}")

if __name__ == "__main__":
    try:
        list_connections()
    except Exception as e:
        print(f"Error: {e}")
