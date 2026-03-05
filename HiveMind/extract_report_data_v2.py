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
# Based on previous output, the description pattern is 'Tiger Brands|Grains|Albany Bakeries|Bellville%'
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
    "generated_at": datetime.datetime.now().isoformat(),
    "points": []
}

# 1. Fetch All Related Points
print(f"Fetching related points for {ROOT_PATTERN}...")
query_points = f"""
    SELECT * 
    FROM `augos-core-data.augos_warehouse.augos_points`
    WHERE Description LIKE '{ROOT_PATTERN}'
"""
points = [dict(row) for row in client.query(query_points).result()]
print(f"Found {len(points)} total points in hierarchy.")

# 2. Iterate and Fetch Detail
financial_search_terms = set()
tariffs_found = set()

for p in points:
    pid = p['PointID']
    p_desc = p['Description']
    
    point_obj = {
        "metadata": p,
        "daily_peaks": []
    }
    
    # Collect search terms for financials
    if p.get('InvoicingEntity'):
        financial_search_terms.add(p['InvoicingEntity'])
    if p.get('TariffID'):
        tariffs_found.add(p['TariffID'])

    # Fetch Usage
    print(f"Fetching usage for {pid}...")
    # SAFEGUARD: Ensure PID is int for this table if schema requires
    try:
        pid_int = int(pid)
        query_usage = f"""
            SELECT *
            FROM `augos-core-data.augos_warehouse.pfc_daily_peaks`
            WHERE PointID = {pid_int}
            ORDER BY Date DESC
            LIMIT 365
        """
        usage = [dict(row) for row in client.query(query_usage).result()]
        point_obj['daily_peaks'] = usage
        if usage:
            print(f"  -> Found {len(usage)} records.")
    except ValueError:
        pass # PID contains chars?
    except Exception as e:
        print(f"  -> Error: {e}")

    data["points"].append(point_obj)

# 3. Fetch Tariffs
data["tariffs"] = []
for tid in tariffs_found:
    print(f"Fetching Tariff {tid}...")
    query_t = f"""
        SELECT * FROM `augos-core-data.augos_warehouse.master_tariffs`
        WHERE TariffID = '{tid}'
    """
    ts = list(client.query(query_t).result())
    if ts:
        data["tariffs"].append(dict(ts[0]))

# 4. Fetch Financials
# If no explicit InvoicingEntity, try "Tiger Brands" or "Albany"
if not financial_search_terms:
    financial_search_terms.add("Tiger Brands")
    financial_search_terms.add("Albany Bakeries")

data["invoices"] = []
for term in financial_search_terms:
    print(f"Fetching Invoices for '{term}'...")
    safe_term = term.replace("'", "\\'")
    query_inv = f"""
        SELECT *
        FROM `augos-core-data.augos_warehouse.xero_invoices`
        WHERE ContactName LIKE '%{safe_term}%'
        ORDER BY Date DESC
        LIMIT 20
    """
    invs = [dict(row) for row in client.query(query_inv).result()]
    data["invoices"].extend(invs)
    print(f"  -> Found {len(invs)} invoices.")

# SAVE
output_path = '/Users/timstevens/Antigravity/HiveMind/energy_report_data.json'
with open(output_path, 'w') as f:
    json.dump(data, f, cls=CustomEncoder, indent=2)

print("Done.")
