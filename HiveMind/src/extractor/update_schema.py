from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
DATASET_ID = 'hive_mind_core'
TABLE_ID = 'staging_raw_emails'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)
table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

def add_column():
    table = client.get_table(table_ref)
    
    # Check if exists
    for schema_field in table.schema:
        if schema_field.name == 'recipient':
            print("Column 'recipient' already exists.")
            return

    new_schema = table.schema[:]
    new_schema.append(bigquery.SchemaField("recipient", "STRING", mode="NULLABLE"))
    
    table.schema = new_schema
    client.update_table(table, ["schema"])
    print("Successfully added 'recipient' column.")

if __name__ == "__main__":
    add_column()
