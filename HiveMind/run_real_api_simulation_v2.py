import json
import decimal
import datetime
from google.cloud import bigquery
import os

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = '/Users/timstevens/Antigravity/HiveMind/credentials/hive-mind-admin.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

client = bigquery.Client(project=PROJECT_ID)

# UPDATED POINT ID FROM USER URL
# URL: https://live.augos.io/app/utilities-and-services/power-factor-and-demand?pointId=37431729
POINT_ID = 37431729 

END_DATE = datetime.datetime.now()
START_DATE = END_DATE - datetime.timedelta(days=365)

# Format as per API requirement (ISO 8601 UTC)
START_DATE_UTC = START_DATE.strftime("%Y-%m-%dT%H:%M:%SZ")
END_DATE_UTC = END_DATE.strftime("%Y-%m-%dT%H:%M:%SZ")

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super(CustomEncoder, self).default(obj)

def run_simulation():
    print(f"Simulating GET /api/v1/power-factor-demand")
    print(f"Query Params: pointID={POINT_ID}, startDateUTC={START_DATE_UTC}, endDateUTC={END_DATE_UTC}")
    
    # We query the warehouse table which backs this API
    query = f"""
        SELECT 
            Date as date,
            PeakKVA as kva,
            KWAtPeak as kw,
            PFAtPeak as powerFactor,
            PeakTimestamp as timestamp
        FROM `augos-core-data.augos_warehouse.pfc_daily_peaks`
        WHERE PointID = {POINT_ID}
          AND PeakTimestamp BETWEEN TIMESTAMP('{START_DATE_UTC}') AND TIMESTAMP('{END_DATE_UTC}')
        ORDER BY PeakTimestamp ASC
    """
    
    data = []
    try:
        rows = list(client.query(query).result())
        data = [dict(row) for row in rows]
    except Exception as e:
        print(f"Error querying BigQuery: {e}")

    # Construct the final JSON response
    response = {
        "request": {
            "endpoint": "/api/v1/power-factor-demand",
            "method": "GET",
            "parameters": {
                "pointID": POINT_ID,
                "startDateUTC": START_DATE_UTC,
                "endDateUTC": END_DATE_UTC
            }
        },
        "response": {
            "count": len(data),
            "data": data
        }
    }
    
    # Save to file
    filepath = '/Users/timstevens/Antigravity/HiveMind/augos_api_response_37431729.json'
    with open(filepath, 'w') as f:
        json.dump(response, f, cls=CustomEncoder, indent=2)
    
    print(f"\nGenerated JSON file: {filepath}")
    if len(data) > 5:
        print(f"First 5 records:\n{json.dumps(data[:5], cls=CustomEncoder, indent=2)}")
    else:
        print(json.dumps(response, cls=CustomEncoder, indent=2))

if __name__ == "__main__":
    run_simulation()
