from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def verify_graph():
    print("Verifying Knowledge Graph...")
    
    # 1. Check Links
    query = """
    SELECT 
        e.name as Entity,
        e.entity_type,
        count(f.message_id) as Linked_Emails
    FROM `augos-core-data.hive_mind_core.fact_email_entities` f
    JOIN `augos-core-data.hive_mind_core.dim_entities` e ON f.entity_id = e.entity_id
    GROUP BY 1, 2
    ORDER BY 3 DESC
    """
    
    rows = list(client.query(query))
    if not rows:
        print("No links found yet.")
    
    for row in rows:
        print(f"🔗 {row.Entity} ({row.entity_type}): {row.Linked_Emails} emails")

if __name__ == "__main__":
    verify_graph()
