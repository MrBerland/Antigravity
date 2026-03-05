from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def check_schema():
    table = client.get_table('augos-core-data.hive_mind_core.staging_raw_emails')
    for field in table.schema:
        if field.name == 'timestamp':
            print(f"Column 'timestamp' is type: {field.field_type}")

if __name__ == "__main__":
    check_schema()
