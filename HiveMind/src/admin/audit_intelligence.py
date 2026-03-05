from google.cloud import bigquery
import os
import json

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

print("--- INTELLIGENCE AUDIT ---")

# 1. Sales Intelligence
print("\n[SALES AGENT]")
q_sales = """
SELECT sales_analysis 
FROM `augos-core-data.hive_mind_core.sales_leads`
WHERE JSON_VALUE(sales_analysis, '$.is_lead') = 'true'
LIMIT 3
"""
try:
    rows = list(client.query(q_sales).result())
    if not rows:
        print("No Hot Leads found yet.")
    else:
        for r in rows:
            print(f"Lead Found: {r.sales_analysis}")
except Exception as e:
    print(f"Error querying sales: {e}")

# 2. Support Intelligence
print("\n[SUPPORT AGENT]")
q_support = """
SELECT analysis_json
FROM `augos-core-data.hive_mind_core.support_thread_scores`
ORDER BY CAST(JSON_VALUE(analysis_json, '$.sentiment_score') AS INT64) DESC
LIMIT 3
"""
try:
    rows = list(client.query(q_support).result())
    if not rows:
        print("No Support Scores found yet.")
    else:
        for r in rows:
            print(f"Support Thread Scored: {r.analysis_json}")
except Exception as e:
    print(f"Error querying support: {e}")


# 3. Workforce Intelligence
print("\n[WORKFORCE AGENT]")
q_work = """
SELECT category, count(*) as count
FROM `augos-core-data.hive_mind_core.fact_work_patterns`
GROUP BY 1
ORDER BY 2 DESC
"""
try:
    rows = list(client.query(q_work).result())
    if not rows:
        print("No Workforce Patterns found yet.")
    else:
        for r in rows:
            print(f"Category: {r.category} ({r.count})")
except Exception as e:
    print(f"Error querying workforce: {e}")
