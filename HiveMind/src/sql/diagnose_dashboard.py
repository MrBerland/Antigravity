from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

print("--- DASHBOARD DIAGNOSTICS ---")

# 1. Check Total Ingested (Should be high)
q1 = "SELECT count(*) as count FROM `augos-core-data.hive_mind_core.staging_raw_emails`"
row1 = list(client.query(q1).result())[0]
print(f"1. Total Ingested Rows: {row1.count}")

# 2. Check AI Processed (might be low due to Streaming Buffer lock)
q2 = "SELECT count(*) as count FROM `augos-core-data.hive_mind_core.messages`"
row2 = list(client.query(q2).result())[0]
print(f"2. PROCESSED Rows (messages table): {row2.count}")

# 3. Check Velocity Data (Email Timestamp vs Ingest Timestamp)
q3 = """
SELECT 
  count(*) as total,
  countif(timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)) as emails_from_last_24h,
  countif(ingest_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)) as ingested_last_24h
FROM `augos-core-data.hive_mind_core.staging_raw_emails`
"""
row3 = list(client.query(q3).result())[0]
print(f"3. Velocity Check:")
print(f"   - Emails Dated Last 24h (Real Traffic): {row3.emails_from_last_24h}")
print(f"   - Emails Ingested Last 24h (System Activity): {row3.ingested_last_24h}")

# 4. Check Processor Status
q4 = """
SELECT processing_status, count(*) as count 
FROM `augos-core-data.hive_mind_core.staging_raw_emails` 
GROUP BY 1
"""
print("4. Processing Status Breakdown:")
rows4 = client.query(q4).result()
for r in rows4:
    print(f"   - {r.processing_status}: {r.count}")
