from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def check_schemas():
    tables = [
        'augos-core-data.augos_warehouse.sites',
        'augos-core-data.augos_warehouse.devices',
        'augos-core-data.augos_warehouse.contacts'
    ]
    
    for table_id in tables:
        print(f"\n--- {table_id} ---")
        try:
            table = client.get_table(table_id)
            for field in table.schema:
                print(f"{field.name} ({field.field_type})")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_schemas()
