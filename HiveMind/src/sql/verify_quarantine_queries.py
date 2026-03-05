from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def verify_quarantine():
    print("Running Quarantine Query Verification...\n")
    
    # Test Cases
    filters = [
        ("ALL", "1=1"), 
        ("PENDING", "processing_status = 'PENDING'"), 
        ("BLOCKED", "security_verdict = 'BLOCK'")
    ]
    
    for label, where_clause in filters:
        print(f"--- Filter: {label} ---")
        q = f"""
        SELECT 
          message_id,
          timestamp,
          sender,
          recipient,
          subject,
          COALESCE(processing_status, 'PENDING') as status,
          COALESCE(security_verdict, 'ALLOW') as verdict
        FROM `augos-core-data.hive_mind_core.staging_raw_emails`
        WHERE {where_clause}
        ORDER BY timestamp DESC
        LIMIT 3
        """
        try:
            rows = list(client.query(q).result())
            for r in rows:
                print(f"  [{r.status}|{r.verdict}] {r.sender} -> {r.recipient}: {r.subject[:30]}")
            
            # Count
            count_q = f"SELECT count(*) as total FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE {where_clause}"
            total = list(client.query(count_q).result())[0].total
            print(f"  Total Count: {total}\n")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    verify_quarantine()
