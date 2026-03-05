from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def deploy_and_test_search():
    # Deploy
    print("Deploying Vector Search Procedure...")
    with open('src/sql/search_vectors.sql', 'r') as f:
        sql = f.read()
    client.query(sql).result()
    print("✅ Deployed.")

    # Test
    term = "billing invoice"
    print(f"Testing Search for '{term}'...")
    query = f"CALL `augos-core-data.hive_mind_core.search_vectors`('{term}', 5)"
    rows = list(client.query(query).result())
    
    for row in rows:
        print(f"🔎 {row.subject} (Dist: {row.distance:.4f})")

if __name__ == "__main__":
    deploy_and_test_search()
