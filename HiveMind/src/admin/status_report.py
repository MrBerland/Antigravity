from google.cloud import bigquery
import os
from datetime import datetime

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

print(f"--- STATUS REPORT {datetime.now()} ---")

# 1. Staging Count
q1 = "SELECT count(*) as count FROM `augos-core-data.hive_mind_core.staging_raw_emails`"
try:
    c1 = list(client.query(q1).result())[0].count
    print(f"📥 Staging Raw Emails: {c1:,}")
except: print("Staging: Error")

# 2. Production Count
q2 = "SELECT count(*) as count FROM `augos-core-data.hive_mind_core.messages`"
try:
    c2 = list(client.query(q2).result())[0].count
    print(f"💾 Production Messages: {c2:,}")
except: print("Messages: Error")

# 3. AI Agents Progress
q_agents = """
SELECT 
    (SELECT count(*) FROM `hive_mind_core.fact_email_entities` WHERE source='GEMINI_ML') as entities,
    (SELECT count(*) FROM `hive_mind_core.fact_work_patterns`) as workforce,
    (SELECT count(*) FROM `hive_mind_core.sales_leads`) as sales,
    (SELECT count(*) FROM `hive_mind_core.support_thread_scores`) as support
"""
try:
    row = list(client.query(q_agents).result())[0]
    print(f"🧠 Entity Extraction: {row.entities:,}")
    print(f"👷 Workforce Analysis: {row.workforce:,}")
    print(f"💼 Sales Leads Found: {row.sales:,}")
    print(f"🆘 Support Threads Scored: {row.support:,}")
except Exception as e:
    print(f"Agent Stats Error: {e}")

# 4. Latest Ingestion Time
q_time = "SELECT max(ingest_time) as last_ingest FROM `augos-core-data.hive_mind_core.staging_raw_emails`"
try:
    t = list(client.query(q_time).result())[0].last_ingest
    print(f"⏱️  Last Ingestion: {t}")
except: print("Time check failed")
