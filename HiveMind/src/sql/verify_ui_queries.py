from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def verify_ui_queries():
    print("running UI Queries Verification...\n")

    # 1. Top Connected Entities
    print("1. Top Connected Entities:")
    q1 = """
    SELECT 
        e.name,
        e.entity_type,
        count(f.message_id) as links
    FROM `augos-core-data.hive_mind_core.fact_email_entities` f
    JOIN `augos-core-data.hive_mind_core.dim_entities` e ON f.entity_id = e.entity_id
    GROUP BY 1, 2
    ORDER BY 3 DESC
    LIMIT 10
    """
    rows1 = list(client.query(q1).result())
    for r in rows1:
        print(f"  - {r.name} ({r.entity_type}): {r.links}")
    if not rows1: print("  (No data yet)")

    # 2. Recent Links
    print("\n2. Recent Links:")
    q2 = """
    SELECT 
        e.name,
        e.entity_type,
        s.subject,
        s.sender,
        f.confidence,
        f.source,
        s.timestamp
    FROM `augos-core-data.hive_mind_core.fact_email_entities` f
    JOIN `augos-core-data.hive_mind_core.dim_entities` e ON f.entity_id = e.entity_id
    JOIN `augos-core-data.hive_mind_core.staging_raw_emails` s ON f.message_id = s.message_id
    ORDER BY s.timestamp DESC
    LIMIT 10
    """
    try:
        rows2 = list(client.query(q2).result())
        for r in rows2:
            print(f"  - {r.timestamp} | {r.name} | {r.subject[:30]}...")
        if not rows2: print("  (No data yet)")
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    verify_ui_queries()
