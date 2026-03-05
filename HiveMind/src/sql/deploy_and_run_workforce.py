from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
# Assuming credentials are in the same spot as the other deploy script
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def execute_file(filepath):
    print(f"Executing {filepath}...")
    with open(filepath, 'r') as f:
        sql = f.read()
        
    job = client.query(sql) 
    job.result() # Wait for completion
    print(f"✅ Success: {filepath}")

def run_analysis():
    print("Running Workforce Analysis Agent...")
    query = "CALL `hive_mind_core.analyze_workforce_patterns`(100);"
    job = client.query(query)
    rows = job.result()
    for row in rows:
        print(f"Result: {row.status}")

if __name__ == "__main__":
    try:
        # Deploy Structure
        execute_file('HiveMind/src/sql/create_workforce_tables.sql')
        # Deploy Logic
        execute_file('HiveMind/src/sql/agent_workforce.sql')
        print("Workforce SQL Deployed.")
        
        # Run It
        run_analysis()
        
    except Exception as e:
        print(f"❌ Operation Failed: {e}")
