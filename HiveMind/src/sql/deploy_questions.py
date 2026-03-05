from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE
client = bigquery.Client(project=PROJECT_ID)

def execute_file(filepath):
    print(f"Executing {filepath}...")
    with open(filepath, 'r') as f:
        sql = f.read()
    job = client.query(sql) 
    job.result()
    print(f"✅ Success: {filepath}")

if __name__ == "__main__":
    try:
        execute_file('HiveMind/src/sql/agent_questions.sql')
    except Exception as e:
        print(f"❌ Failed: {e}")
