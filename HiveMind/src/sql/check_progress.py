from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

query = """
SELECT 
  (SELECT count(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails`) as staging_count,
  (SELECT count(*) FROM `augos-core-data.hive_mind_core.fact_work_patterns`) as workforce_count,
  (SELECT count(*) FROM `augos-core-data.hive_mind_core.fact_email_entities` WHERE source='GEMINI_ML') as semantic_entities
"""

try:
    rows = client.query(query).result()
    for row in rows:
        print(f"STAGING: {row.staging_count}")
        print(f"WORKFORCE: {row.workforce_count}")
        print(f"SEMANTIC: {row.semantic_entities}")
except Exception as e:
    print(f"Error checking progress: {e}")
