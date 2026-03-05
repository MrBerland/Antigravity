from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def verify_ops_queries():
    print("running Ops Queries Verification...\n")

    print("Querying view_ops_bottlenecks:")
    q = """
      SELECT *
      FROM `augos-core-data.hive_mind_core.view_ops_bottlenecks`
      ORDER BY friction_score DESC
      LIMIT 10
    """
    try:
        rows = list(client.query(q).result())
        for r in rows:
            print(f"  - [{r.friction_score}] {r.subject[:40]}... ({r.status})")
        if not rows: print("  (No bottlenecks found yet)")
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    verify_ops_queries()
