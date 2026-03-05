from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def run_semantic_extraction():
    print("Running Semantic Extraction (Batch Size: 5)...")
    query = "CALL `augos-core-data.hive_mind_core.extract_entities_semantic`(5)"
    
    job = client.query(query)
    rows = list(job.result())
    
    if rows:
        print(f"✅ {rows[0].status}")
    else:
        print("✅ Procedure ran but returned no status row.")

def verify_ml_results():
    print("\nVerifying ML Extracted Entities:")
    query = """
    SELECT 
        e.name,
        e.entity_type,
        f.confidence,
        s.subject
    FROM `augos-core-data.hive_mind_core.fact_email_entities` f
    JOIN `augos-core-data.hive_mind_core.dim_entities` e ON f.entity_id = e.entity_id
    JOIN `augos-core-data.hive_mind_core.staging_raw_emails` s ON f.message_id = s.message_id
    WHERE f.source = 'GEMINI_ML'
    LIMIT 5
    """
    rows = list(client.query(query))
    if not rows:
        print("No ML entities found just yet.")
    for row in rows:
        print(f"🤖 Found '{row.name}' ({row.entity_type}) in '{row.subject}'")

if __name__ == "__main__":
    run_semantic_extraction()
    verify_ml_results()
