import json
import decimal
import datetime
from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

POINT_ID = '10267'

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super(CustomEncoder, self).default(obj)

data = {
    "target_point_id": POINT_ID,
    "generated_at": datetime.datetime.now().isoformat(),
    "sources": {}
}

# 1. Fetch Point Metadata
print("Fetching Point Metadata...")
query_point = f"""
    SELECT * 
    FROM `augos-core-data.augos_warehouse.augos_points`
    WHERE PointID = '{POINT_ID}'
"""
points = list(client.query(query_point).result())
if points:
    point_data = dict(points[0])
    data["point_metadata"] = point_data
    print(f"Found Point: {point_data.get('Description')}")
    
    # Use info for further queries
    tariff_id = point_data.get('TariffID')
    xero_contact_id = point_data.get('XeroContactID')
    invoicing_entity = point_data.get('InvoicingEntity') # Name of debtor
else:
    print("Point not found!")
    point_data = {}

# 2. Fetch Tariff
if point_data.get('TariffID'):
    print(f"Fetching Tariff {point_data['TariffID']}...")
    query_tariff = f"""
        SELECT *
        FROM `augos-core-data.augos_warehouse.master_tariffs`
        WHERE TariffID = '{point_data['TariffID']}'
    """
    tariffs = list(client.query(query_tariff).result())
    if tariffs:
        data["tariff"] = dict(tariffs[0])

# 3. Fetch Demand/Usage Data (PFC Peaks)
print("Fetching Demand Data (PFC Peaks)...")
# Note: PointID is Integer in pfc_daily_peaks
query_pfc = f"""
    SELECT *
    FROM `augos-core-data.augos_warehouse.pfc_daily_peaks`
    WHERE PointID = {POINT_ID}
    ORDER BY Date DESC
    LIMIT 365
"""
try:
    pfc_data = [dict(row) for row in client.query(query_pfc).result()]
    data["demand_profile_daily"] = pfc_data
    print(f"Fetched {len(pfc_data)} daily peak records.")
except Exception as e:
    print(f"Error fetching PFC data: {e}")
    data["demand_profile_daily_error"] = str(e)

# 4. Fetch Financials (Invoices)
if point_data.get('InvoicingEntity'):
    entity_name = point_data['InvoicingEntity']
    print(f"Fetching Invoices for {entity_name}...")
    # Escape single quotes in name just in case
    safe_name = entity_name.replace("'", "\\'")
    query_invoices = f"""
        SELECT *
        FROM `augos-core-data.augos_warehouse.xero_invoices`
        WHERE ContactName LIKE '%{safe_name}%'
        ORDER BY Date DESC
        LIMIT 50
    """
    invoices = [dict(row) for row in client.query(query_invoices).result()]
    data["financials_invoices"] = invoices
    print(f"Fetched {len(invoices)} invoices.")

# 5. Fetch Related Sites/Context
# Search for similar names in Sites or Points
print("Fetching Contextual Data...")
query_context = f"""
    SELECT PointID, Description, IsSite
    FROM `augos-core-data.augos_warehouse.augos_points`
    WHERE Description LIKE '%Albany%' AND Description LIKE '%Bellville%'
    LIMIT 10
"""
context_points = [dict(row) for row in client.query(query_context).result()]
data["related_points"] = context_points

# SAVE TO FILE
output_path = '/Users/timstevens/Antigravity/HiveMind/energy_report_data.json'
with open(output_path, 'w') as f:
    json.dump(data, f, cls=CustomEncoder, indent=2)

print(f"Done. Data saved to {output_path}")
