from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def deploy_and_run():
    # 1. Deploy Procedure
    print("Deploying Sync Procedure...")
    with open('HiveMind/src/sql/sync_entities.sql', 'r') as f:
        sql = f.read()
    job = client.query(sql)
    job.result()
    print("✅ Procedure Deployed.")

    # 2. Run Procedure
    print("Running Entity Sync (Pulling from Warehouse)...")
    job = client.query("CALL `augos-core-data.hive_mind_core.sync_entities`()")
    rows = list(job.result())
    p_status = rows[0].status if rows else "Unknown"
    print(f"✅ Sync Complete: {p_status}")

if __name__ == "__main__":
    deploy_and_run()
