import json
import decimal
import datetime
from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

# API Parameters
POINT_ID = 10267
ENDPOINT = "/api/v1/power-factor-demand"

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super(CustomEncoder, self).default(obj)

def run_query():
    print(f"Executing Query for {ENDPOINT} (PointID: {POINT_ID})...")
    
    # Logic: Get last 12 months of daily peaks
    query = f"""
        SELECT 
            Date,
            PeakKVA as demand_kva,
            KWAtPeak as demand_kw,
            PFAtPeak as power_factor,
            PeakTimestamp
        FROM `augos-core-data.augos_warehouse.pfc_daily_peaks`
        WHERE PointID = {POINT_ID}
          AND Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
        ORDER BY Date ASC
    """
    
    try:
        rows = list(client.query(query).result())
        data = [dict(row) for row in rows]
        
        response = {
            "endpoint": ENDPOINT,
            "params": {
                "point_id": POINT_ID,
                "period": "12_months"
            },
            "meta": {
                "count": len(data),
                "generated_at": datetime.datetime.now().isoformat()
            },
            "data": data
        }
        
        print(json.dumps(response, cls=CustomEncoder, indent=2))
        
    except Exception as e:
        error_resp = {
            "error": "Internal Server Error",
            "message": str(e)
        }
        print(json.dumps(error_resp, indent=2))

if __name__ == "__main__":
    run_query()
