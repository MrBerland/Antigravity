from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

print(" Debugging Workforce Agent Logic...")

# 1. Check Pending Count
query_pending = """
SELECT count(*) as count
FROM `augos-core-data.hive_mind_core.staging_raw_emails`
WHERE 
    sender LIKE '%' 
    AND message_id NOT IN (SELECT message_id FROM `augos-core-data.hive_mind_core.fact_work_patterns`)
"""
print("Checking pending candidates...")
rows = client.query(query_pending).result()
for row in rows:
    print(f"Pending Candidates (Ready for AI): {row.count}")

# 2. Run a Test AI Call (on 1 row)
query_ai = """
SELECT 
    message_id, 
    ml_generate_text_result 
FROM ML.GENERATE_TEXT(
    MODEL `augos-core-data.hive_mind_core.gemini_flash`,
    (
        SELECT message_id, 'Classify this email: ' || snippet as prompt
        FROM `augos-core-data.hive_mind_core.staging_raw_emails`
        LIMIT 1
    ),
    STRUCT(0.0 AS temperature, TRUE AS flatten_json_output)
)
"""
print("Testing Model Connection (Gemini Flash)...")
try:
    rows = client.query(query_ai).result()
    for row in rows:
        print(f"AI Response: {row.ml_generate_text_result[:100]}...") # Print first 100 chars
except Exception as e:
    print(f"AI Execution Failed: {e}")
