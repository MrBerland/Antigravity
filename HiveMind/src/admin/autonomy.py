import time
import subprocess
import os
import sys
from datetime import datetime

# Set Environment for sub-processes
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def run_script_bg(script_path):
    log(f"🚀 Launching Background Process: {script_path}...")
    try:
        # Popen is non-blocking
        process = subprocess.Popen(
            ['python3', script_path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        return process
    except Exception as e:
        log(f"❌ Error launching {script_path}: {e}")
        return None

def run_query(client, query):
    try:
        rows = list(client.query(query).result())
        if rows:
            return rows[0].count
        return 0
    except Exception as e:
        log(f"Query Error: {e}")
        return 0

if __name__ == "__main__":
    log("🤖 Hive Mind Autonomy Engine Started.")
    
    # 1. Trigger Initial Backfill (Background Mode)
    # We launch ingestion ensuring it runs in parallel with analysis
    log("Phase 1: Launching Continuous Ingestion (Background)...")
    ingestion_process = run_script_bg('HiveMind/src/extractor/fast_backfill.py')
    
    # 2. Infinite Processing Loop
    log("Phase 2: Entering Parallel AI Processing Loop...")
    
    # Lazy load BQ client
    from google.cloud import bigquery
    client = bigquery.Client()
    
    while True:
        try:
            # Check Ingestion Health
            if ingestion_process:
                ret = ingestion_process.poll()
                if ret is not None:
                    log(f"⚠️ Ingestion Process stopped with code {ret}. Restarting...")
                    ingestion_process = run_script_bg('HiveMind/src/extractor/fast_backfill.py')

            # A. Process Staging -> Production
            # Promote any new arriving emails (Push or Pull)
            log("Core: Promoting Staging Data...")
            run_query(client, "CALL `hive_mind_core.process_staging_data`();")
            
            # B. Check for Pending Work
            # 1. Semantic Extraction
            pending_semantic = run_query(client, """
                SELECT count(*) as count 
                FROM `hive_mind_core.messages` m
                WHERE NOT EXISTS (SELECT 1 FROM `hive_mind_core.fact_email_entities` f WHERE f.message_id = m.message_id AND source='GEMINI_ML')
                LIMIT 1
            """)
            
            if pending_semantic > 0:
                log(f"Brain: Extracting Entities ({pending_semantic} pending)...")
                # Run batch of 200
                run_query(client, "CALL `hive_mind_core.extract_entities_semantic`(200);")
            else:
                log("Brain: Semantic Extraction Up to Date.")

            # 2. Workforce Analysis
            pending_workforce = run_query(client, """
                SELECT count(*) as count 
                FROM `hive_mind_core.staging_raw_emails` m
                WHERE sender LIKE '%' 
                AND message_id NOT IN (SELECT message_id FROM `hive_mind_core.fact_work_patterns`)
                LIMIT 1
            """)
            
            if pending_workforce > 0:
                log(f"Brain: Analyzing Workforce Patterns ({pending_workforce} pending)...")
                # Run batch of 500
                run_query(client, "CALL `hive_mind_core.analyze_workforce_patterns`(500);")
            else:
                log("Brain: Workforce Analysis Up to Date.")

            # 3. Sales Leads
            pending_sales = run_query(client, """
                SELECT count(*) as count 
                FROM `hive_mind_core.messages` m
                WHERE sender NOT LIKE '%@augos.io' 
                AND message_id NOT IN (SELECT message_id FROM `hive_mind_core.sales_leads`)
                LIMIT 1
            """)
            
            if pending_sales > 0:
                log(f"Brain: Hunting Sales Leads ({pending_sales} pending)...")
                run_query(client, "CALL `hive_mind_core.analyze_sales_leads`(200);")
            else:
                log("Brain: Sales Analysis Up to Date.")

            # 4. Support Threads
            # Logic: Check threads updated recently that haven't been scored
            pending_support = run_query(client, """
                SELECT count(*) as count 
                FROM `hive_mind_core.messages` m
                WHERE thread_id NOT IN (SELECT thread_id FROM `hive_mind_core.support_thread_scores`)
                LIMIT 1
            """)
            
            if pending_support > 0:
                log(f"Brain: Scoring Support Threads ({pending_support} pending)...")
                run_query(client, "CALL `hive_mind_core.analyze_support_threads`(50);")
            else:
                log("Brain: Support Analysis Up to Date.")

            # 5. Question & Inefficiency Analysis
            pending_questions = run_query(client, """
                SELECT count(*) as count 
                FROM `hive_mind_core.messages` m
                WHERE sender NOT LIKE '%@augos.io' 
                AND message_id NOT IN (SELECT message_id FROM `hive_mind_core.fact_questions`)
                LIMIT 1
            """)

            if pending_questions > 0:
                log(f"Brain: Extracting Questions ({pending_questions} pending)...")
                run_query(client, "CALL `hive_mind_core.analyze_questions`(50);")
            else:
                log("Brain: Question Analysis Up to Date.")
            
            # Sleep before next cycle
            sleep_time = 60
            log(f"💤 Sleeping {sleep_time}s...")
            time.sleep(sleep_time)
            
        except KeyboardInterrupt:
            log("🛑 Autonomy Stopped by User.")
            break
        except Exception as e:
            log(f"❌ Critical Autonomy Error: {e}")
            time.sleep(60) # Wait and retry
