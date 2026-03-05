from google.cloud import bigquery
import os
import time

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def run_sql_file(file_path):
    with open(file_path, 'r') as f:
        sql = f.read()
    client.query(sql).result()
    print(f"✅ Executed {file_path}")

def run_embeddings():
    # 1. Deploy Model
    run_sql_file('src/sql/create_embedding_model.sql')
    
    # 2. Deploy Procedure
    run_sql_file('src/sql/generate_embeddings.sql')
    
    # 3. Run Generation
    print("Running Embedding Generation (Batch: 50)...")
    query = "CALL `augos-core-data.hive_mind_core.generate_embeddings`(50)"
    try:
        rows = list(client.query(query).result())
        if rows:
            print(f"✅ {rows[0].status}")
    except Exception as e:
        print(f"❌ Error running generation: {e}")

    # 4. Verify Count
    count_query = "SELECT count(*) as count FROM `augos-core-data.hive_mind_core.fact_embeddings`"
    rows = list(client.query(count_query).result())
    print(f"📊 Total Embeddings: {rows[0].count}")

if __name__ == "__main__":
    run_embeddings()
