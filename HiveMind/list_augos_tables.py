from google.cloud import bigquery
import os
import json

# Env Config
PROJECT_ID = 'augos-core-data'
# We need credentials. explore_bq.py referenced 'HiveMind/credentials/hive-mind-admin.json'
# I need to make sure this file exists. 
# But usually in this environment, I might not have access to that specific file location if it's not relative.
# explore_bq.py used os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
# Let's check if that file exists.

SERVICE_ACCOUNT_FILE = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def list_tables(dataset_id):
    print(f"Tables in dataset {dataset_id}:")
    tables = list(client.list_tables(dataset_id))
    if tables:
        for table in tables:
            print(f"\t{table.table_id}")
    else:
        print("\tNone found.")

if __name__ == "__main__":
    list_tables('augos_warehouse')
