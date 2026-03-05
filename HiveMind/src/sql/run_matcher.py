from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def run_matcher():
    print("Running Entity Matcher Procedure...")
    query = "CALL `augos-core-data.hive_mind_core.match_entities`()"
    
    job = client.query(query)
    # Fetch result to ensure it completes, though procedures might return rows
    result = list(job.result())
    
    for row in result:
        print(row)
    
    print("✅ Matcher Complete.")

if __name__ == "__main__":
    run_matcher()
