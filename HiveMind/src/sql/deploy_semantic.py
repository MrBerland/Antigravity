from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def deploy_semantic():
    print("Deploying Semantic Extraction Procedure...")
    with open('HiveMind/src/sql/extract_entities_semantic.sql', 'r') as f:
        sql = f.read()
    
    job = client.query(sql)
    job.result()
    print("✅ Procedure Deployed.")

if __name__ == "__main__":
    deploy_semantic()
