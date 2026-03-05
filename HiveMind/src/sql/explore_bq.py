from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def list_datasets():
    print(f"Datasets in project {PROJECT_ID}:")
    datasets = list(client.list_datasets())
    if datasets:
        for dataset in datasets:
            print(f"\t{dataset.dataset_id}")
    else:
        print("\tNone found.")

if __name__ == "__main__":
    list_datasets()
