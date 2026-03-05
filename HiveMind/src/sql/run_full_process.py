from google.cloud import bigquery
import os
import time

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def run_query(query, description):
    print(f"🔹 Starting: {description}")
    start = time.time()
    try:
        job = client.query(query)
        result = job.result() # Wait for completion
        duration = time.time() - start
        
        # Try to print status if returned
        status = None
        for row in result:
             # Look for a 'status' column or similar if the proc returns it
             if hasattr(row, 'status'):
                 status = row.status
        
        print(f"✅ Completed: {description} in {duration:.2f}s")
        if status:
            print(f"   Status: {status}")
            
    except Exception as e:
        print(f"❌ Failed: {description}")
        print(f"   Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Hive Mind Full Processing Cycle...")

    # 1. Promote Staging -> Production & Run Basic Matcher
    # This invokes 'process_staging_data' and 'match_entities'
    run_query("CALL `hive_mind_core.process_staging_data`();", "Process Staging & Basic Match")

    # 2. Run Semantic Extraction (Gemini Flash)
    # INCREASED LIMIT for 'Fully Process' request
    run_query("CALL `hive_mind_core.extract_entities_semantic`(200);", "Semantic Entity Extraction")
    
    # 3. Run Workforce Analysis (Gemini Flash)
    # INCREASED LIMIT for 'Fully Process' request
    run_query("CALL `hive_mind_core.analyze_workforce_patterns`(500);", "Workforce Pattern Analysis")
    
    print("🏁 Processing Cycle Complete.")
