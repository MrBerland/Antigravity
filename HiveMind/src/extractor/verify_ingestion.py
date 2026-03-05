from google.cloud import bigquery
import os

# Env Config
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

def verify():
    print("running verification...")
    # 1. Check Total Count & Missing Recipients
    query1 = """
    SELECT 
      count(*) as total_rows, 
      countif(recipient is null) as null_recipients
    FROM `augos-core-data.hive_mind_core.staging_raw_emails`
    """
    rows1 = list(client.query(query1))
    print(f"Total Rows: {rows1[0].total_rows}")
    print(f"Null Recipients: {rows1[0].null_recipients}")
    print(f"Populated Recipients: {rows1[0].total_rows - rows1[0].null_recipients}")

    # 2. Check Distribution
    query2 = """
    SELECT recipient, count(*) as count 
    FROM `augos-core-data.hive_mind_core.staging_raw_emails` 
    GROUP BY 1 
    ORDER BY 2 DESC 
    LIMIT 5
    """
    print("\nTop Recipients:")
    for row in client.query(query2):
        print(f"{row.recipient}: {row.count}")

if __name__ == "__main__":
    verify()
