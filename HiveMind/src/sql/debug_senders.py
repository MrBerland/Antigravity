from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

query = """
SELECT 
    sender, 
    count(*) as count 
FROM `augos-core-data.hive_mind_core.staging_raw_emails`
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10
"""

print("running sender check...")
rows = client.query(query).result()
for row in rows:
    print(f"{row.sender}: {row.count}")
