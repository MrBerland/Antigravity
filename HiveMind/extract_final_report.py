import json
import decimal
import datetime
from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

ROOT_POINT_ID = '10267'
ROOT_PATTERN = 'Tiger Brands|Grains|Albany Bakeries|Bellville%'

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super(CustomEncoder, self).default(obj)

data = {
    "site_id": ROOT_POINT_ID, 
    "site_name": "Tiger Brands - Bellville",
    "generated_at": datetime.datetime.now().isoformat(),
    "points": [],
    "financials": [],
    "data_quality_report": {
        "consumption_data_found": False,
        "tariffs_found": False
    }
}

# 1. Fetch Points
print(f"Fetching related points for {ROOT_PATTERN}...")
query_points = f"""
    SELECT * 
    FROM `augos-core-data.augos_warehouse.augos_points`
    WHERE Description LIKE '{ROOT_PATTERN}'
"""
points = [dict(row) for row in client.query(query_points).result()]

serial_numbers = []

for p in points:
    pid = p['PointID']
    serial = p.get('SerialNumber')
    if serial:
        serial_numbers.append(serial)
    
    point_obj = {
        "metadata": p,
        "device_summary": None
    }
    data["points"].append(point_obj)

# 2. Fetch Device Summary (if available)
if serial_numbers:
    quoted_serials = ",".join([f"'{s}'" for s in serial_numbers])
    print(f"Fetching device summary for serials: {quoted_serials}...")
    query_dev = f"""
        SELECT *
        FROM `augos-core-data.augos_warehouse.device_summary`
        WHERE SerialNumber IN ({quoted_serials})
    """
    try:
        dev_summaries = [dict(row) for row in client.query(query_dev).result()]
        # Map back to points
        for ds in dev_summaries:
            s_num = ds['SerialNumber']
            for p_obj in data["points"]:
                if p_obj['metadata'].get('SerialNumber') == s_num:
                    p_obj['device_summary'] = ds
        print(f"Found {len(dev_summaries)} device summaries.")
    except Exception as e:
        print(f"Error checking device summary: {e}")

# 3. Fetch Invoices AND Line Items
print("Fetching Invoices and Line Items...")
# We found InvoiceID '34c6a34e-f118-4588-a4fe-f8ade118926b' earlier via loose search.
# Let's search loosely again but include line items.
query_inv = f"""
    SELECT *
    FROM `augos-core-data.augos_warehouse.xero_invoices`
    WHERE ContactName LIKE '%Tiger Brands%' OR ContactName LIKE '%Albany Bakeries%'
    ORDER BY Date DESC
    LIMIT 20
"""
invoices = [dict(row) for row in client.query(query_inv).result()]
for inv in invoices:
    inv_id = inv['InvoiceID']
    query_lines = f"""
        SELECT * FROM `augos-core-data.augos_warehouse.xero_line_items`
        WHERE InvoiceID = '{inv_id}'
    """
    lines = [dict(row) for row in client.query(query_lines).result()]
    inv['line_items'] = lines

data["financials"] = invoices

# SAVE
output_path = '/Users/timstevens/Antigravity/HiveMind/final_energy_report.json'
with open(output_path, 'w') as f:
    json.dump(data, f, cls=CustomEncoder, indent=2)

print(f"Done. Report saved to {output_path}")
