from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

tables = [
    'augos_warehouse.revenue_summary',
    'augos_warehouse.xero_invoices'
]

for table_id in tables:
    try:
        table = client.get_table(table_id)
        print(f"\nSchema for {table_id}:")
        for schema in table.schema:
            print(f"\t{schema.name} ({schema.field_type})")
    except Exception as e:
        print(f"Error getting schema for {table_id}: {e}")
