from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def execute_file(filepath):
    print(f"Executing {filepath}...")
    with open(filepath, 'r') as f:
        sql = f.read()
        
    # Split by semicolon if multiple statements? 
    # The BQ client executes one job per query string usually.
    # create_entity_tables.sql has multiple statements (CREATE x2, INSERT).
    # We should split them or leave them if BQ scripting is enabled.
    # Procedural SQL (BEGIN...END) handles blocks.
    
    # Simple split strategy for avoiding "Multiple statements" error if not using script job
    # Job config - ensure we wait
    job = client.query(sql) 
    job.result() # Wait for completion
    print(f"✅ Success: {filepath}")

if __name__ == "__main__":
    try:
        execute_file('HiveMind/src/sql/create_entity_tables.sql')
        execute_file('HiveMind/src/sql/match_entities.sql')
        print("Knowledge Graph SQL Deployed.")
    except Exception as e:
        print(f"❌ Deployment Failed: {e}")
