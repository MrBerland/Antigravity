from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def debug_schema():
    print("Debugging ML Model Schema...")
    query = """
    SELECT *
    FROM ML.GENERATE_TEXT(
      MODEL `augos-core-data.hive_mind_core.gemini_flash`,
      (SELECT 'Hello' as prompt),
      STRUCT(10 as max_output_tokens)
    )
    LIMIT 1
    """
    
    try:
        job = client.query(query)
        result = list(job.result())
        print("✅ Query Successful. Columns found:")
        for row in result:
            print(row.keys())
            # Also print specific content to be sure
            # print(row)
    except Exception as e:
        print(f"❌ Query Failed: {e}")

if __name__ == "__main__":
    debug_schema()
