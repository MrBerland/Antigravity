from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def list_all():
    print(f"Datasets in project {PROJECT_ID}:")
    datasets = list(client.list_datasets())
    if datasets:
        for dataset in datasets:
            ds_id = dataset.dataset_id
            print(f"\nDataset: {ds_id}")
            tables = list(client.list_tables(ds_id))
            if tables:
                for table in tables:
                    print(f"\tTable: {table.table_id}")
            else:
                print("\t(No tables)")
    else:
        print("\tNone found.")

if __name__ == "__main__":
    list_all()
