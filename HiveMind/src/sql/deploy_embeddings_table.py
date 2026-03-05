from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def deploy_embeddings_table():
    print("Deploying Embeddings Table...")
    with open('HiveMind/src/sql/create_embeddings_table.sql', 'r') as f:
        sql = f.read()
    
    client.query(sql).result()
    print("✅ Table Deployed.")

if __name__ == "__main__":
    deploy_embeddings_table()
