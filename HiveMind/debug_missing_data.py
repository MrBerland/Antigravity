from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

INVOICE_ID = '34c6a34e-f118-4588-a4fe-f8ade118926b'

print("--- PFC PEAKS SAMPLE ---")
query_peaks = """
    SELECT * FROM `augos-core-data.augos_warehouse.pfc_daily_peaks`
    LIMIT 5
"""
try:
    peaks = list(client.query(query_peaks).result())
    for p in peaks:
        print(dict(p))
except Exception as e:
    print(f"Error fetching peaks: {e}")

print("\n--- INVOICE LINE ITEMS ---")
query_lines = f"""
    SELECT * FROM `augos-core-data.augos_warehouse.xero_line_items`
    WHERE InvoiceID = '{INVOICE_ID}'
"""
try:
    lines = list(client.query(query_lines).result())
    for l in lines:
        print(dict(l))
except Exception as e:
    print(f"Error fetching lines: {e}")
