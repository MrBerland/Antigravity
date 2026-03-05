from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

tables = [
    'augos_warehouse.device_summary',
    'augos_warehouse.pfc_compliance'
]

for table_id in tables:
    try:
        table = client.get_table(table_id)
        print(f"\nSchema for {table_id}:")
        for schema in table.schema:
            print(f"\t{schema.name} ({schema.field_type})")
    except Exception as e:
        print(f"Error getting schema for {table_id}: {e}")

print("\n--- CHECKING USAGE DATA ---")
point_ids = [
    10267, 37431744, 37431729, 48951750, 37431760, 
    10270, 10269, 37431745, 10268, 48951778
]
ids_str = ",".join(str(i) for i in point_ids)

query_check = f"""
    SELECT PointID, COUNT(*) as count, MIN(Date) as first_date, MAX(Date) as last_date
    FROM `augos-core-data.augos_warehouse.pfc_daily_peaks`
    WHERE PointID IN ({ids_str})
    GROUP BY PointID
"""
try:
    rows = list(client.query(query_check).result())
    if rows:
        print("Found data:")
        for r in rows:
            print(dict(r))
    else:
        print("No rows found in pfc_daily_peaks for these IDs.")
except Exception as e:
    print(f"Error checking usage: {e}")

print("\n--- CHECKING GLOBAL USAGE ---")
# Just to sanity check the table isn't empty
query_global = "SELECT COUNT(*) as total FROM `augos-core-data.augos_warehouse.pfc_daily_peaks`"
res = list(client.query(query_global).result())
print(f"Total rows in pfc_daily_peaks: {res[0]['total']}")
