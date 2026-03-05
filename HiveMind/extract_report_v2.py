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
# Based on previous output
ROOT_PATTERN = 'Tiger Brands|Grains|Albany Bakeries|Bellville%'

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super(CustomEncoder, self).default(obj)

data = {
    "report_context": {
        "site_id": ROOT_POINT_ID,
        "site_name": "Tiger Brands - Bellville",
        "generated_at": datetime.datetime.now().isoformat(),
        "requested_sections": [
            "Bill Verification", "Load Profile (12m)", "Power Factor", "Cost Breakdown", "Consumption Breakdown"
        ]
    },
    "asset_registry": [],
    "financial_data": {
        "invoices": [],
        "cost_breakdown": {
            "monitoring_fees": 0.0,
            "curtailment_fees": 0.0,
            "usage_charges": 0.0,
            "other": 0.0,
            "total_billed": 0.0
        }
    },
    "telemetry_data": {
        "status": "MISSING",
        "notes": "No daily peak or consumption entries found in augos_warehouse.pfc_daily_peaks.",
        "pfc_compliance": None
    }
}

# 1. FETCH ASSETS
print(f"Fetching asset hierarchy for {ROOT_PATTERN}...")
query_points = f"""
    SELECT * 
    FROM `augos-core-data.augos_warehouse.augos_points`
    WHERE Description LIKE '{ROOT_PATTERN}'
"""
points = [dict(row) for row in client.query(query_points).result()]
for p in points:
    data["asset_registry"].append(p)

# 2. FETCH FINANCIALS & CATEGORIZE
print("Fetching and categorizing financials...")
query_inv = f"""
    SELECT *
    FROM `augos-core-data.augos_warehouse.xero_invoices`
    WHERE ContactName LIKE '%Tiger Brands%' OR ContactName LIKE '%Albany Bakeries%'
    ORDER BY Date DESC
    LIMIT 50
"""
invoices = [dict(row) for row in client.query(query_inv).result()]
processed_invoices = []

for inv in invoices:
    inv_id = inv['InvoiceID']
    # Fetch lines
    query_lines = f"""
        SELECT * FROM `augos-core-data.augos_warehouse.xero_line_items`
        WHERE InvoiceID = '{inv_id}'
    """
    lines = [dict(row) for row in client.query(query_lines).result()]
    inv['line_items'] = lines
    
    # Categorize Costs
    for line in lines:
        amount = float(line.get('LineAmount') or 0.0)
        desc = (line.get('Description') or '').lower()
        
        data['financial_data']['cost_breakdown']['total_billed'] += amount
        
        if 'monitoring' in desc:
            data['financial_data']['cost_breakdown']['monitoring_fees'] += amount
        elif 'curtailment' in desc:
             data['financial_data']['cost_breakdown']['curtailment_fees'] += amount
        elif 'usage' in desc or 'kwh' in desc:
             data['financial_data']['cost_breakdown']['usage_charges'] += amount
        else:
             data['financial_data']['cost_breakdown']['other'] += amount
             
    processed_invoices.append(inv)

data['financial_data']['invoices'] = processed_invoices

# 3. CHECK COMPLIANCE (Just in case)
print("Checking PFC Compliance for context...")
pids = [str(p['PointID']) for p in points]
if pids:
    pids_str = ",".join(pids)
    query_comp = f"""
        SELECT * FROM `augos-core-data.augos_warehouse.pfc_compliance`
        WHERE PointID IN ({pids_str})
    """
    try:
        comps = [dict(row) for row in client.query(query_comp).result()]
        data['telemetry_data']['pfc_compliance'] = comps
    except:
        pass

# SAVE
output_path = '/Users/timstevens/Antigravity/HiveMind/energy_report_final_v2.json'
with open(output_path, 'w') as f:
    json.dump(data, f, cls=CustomEncoder, indent=2)

print(f"Done. Detailed report saved to {output_path}")
