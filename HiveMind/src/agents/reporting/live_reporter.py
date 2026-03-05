import os
import json
import requests
import datetime
import argparse
from typing import Dict, Any, List

# Configuration
API_BASE_URL = "https://live.augos.io/api/v1"  # Or "https://api.augos.io/api/v1" - confirming based on UI URL

class AugosLiveReporter:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def fetch_json(self, endpoint: str, params: Dict[str, Any] = None) -> Any:
        url = f"{API_BASE_URL}{endpoint}"
        try:
            print(f"  -> Fetching {endpoint}...")
            resp = requests.get(url, headers=self.headers, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"  [!] Error fetching {url}: {e}")
            if e.response is not None:
                print(f"      Response: {e.response.text}")
            return None

    def generate_site_report(self, point_id: int) -> Dict[str, Any]:
        """
        Builds the complete Energy Management Report by aggregating live API calls.
        """
        print(f"Starting Live Report Generation for PointID: {point_id}")
        
        # 1. Define Time Windows
        now = datetime.datetime.utcnow()
        date_format = "%Y-%m-%dT%H:%M:%S.000Z"
        
        end_date = now
        start_date_12m = now - datetime.timedelta(days=365)
        
        start_str = start_date_12m.strftime(date_format)
        end_str = end_date.strftime(date_format)
        
        report = {
            "metadata": {
                "point_id": point_id,
                "generated_at": now.isoformat(),
                "data_source": "Augos Live API",
                "period": "Last 12 Months"
            },
            "site_info": {},
            "hierarchy": [],
            "telemetry": {
                "power_factor_demand": {},
                "consumption": {}
            },
            "financials": {
                "cost_breakdown": {},
                "invoices": []
            }
        }

        # 2. Fetch Point Metadata & Hierarchy
        print("Fetching Point Metadata...")
        meta = self.fetch_json(f"/measurement/points/point", {"pointId": point_id})
        if meta:
            report["site_info"] = meta
        
        # 3. Fetch Power Factor & Demand (12 Months)
        # Endpoint identified: /api/v1/power-factor-demand
        print("Fetching Power Factor & Demand Data...")
        pf_params = {
            "pointId": point_id,
            "startDateUTC": start_str,
            "endDateUTC": end_str
        }
        pf_data = self.fetch_json("/power-factor-demand", pf_params)
        if pf_data:
            report["telemetry"]["power_factor_demand"] = pf_data

        # 4. Fetch Consumption Breakdown
        # Endpoint estimated: /api/v1/consumption-breakdown
        print("Fetching Consumption Breakdown...")
        cons_params = {
            "pointId": point_id, 
            "startDateUTC": start_str,
            "endDateUTC": end_str,
            "interval": "month" # Assuming generic parameter for aggregation
        }
        cons_data = self.fetch_json("/consumption-breakdown", cons_params)
        if cons_data:
            report["telemetry"]["consumption"] = cons_data

        # 5. Fetch Cost Breakdown
        # Endpoint estimated: /api/v1/cost-breakdown
        print("Fetching Cost Breakdown...")
        cost_params = {
            "pointId": point_id,
            # "productTypeId": 1, # Electricity often 1, might need to guess or fetch types
            "startDateUTC": start_str,
            "endDateUTC": end_str
        }
        cost_data = self.fetch_json("/cost-breakdown", cost_params)
        if cost_data:
            report["financials"]["cost_breakdown"] = cost_data

        # 6. Fetch Bills/Invoices (Verification)
        # Endpoint: /api/v1/bills-verification/bill-list
        print("Fetching Bill Verification Data...")
        bill_params = {
            "pointId": point_id,
            "startDateUTC": start_str,
            "endDateUTC": end_str
        }
        bills = self.fetch_json("/bills-verification/bill-list", bill_params)
        if bills and isinstance(bills, list):
            report["financials"]["invoices"] = bills[:12] # Last 12 bills

        return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Augos Live Energy Report")
    parser.add_argument("--point", type=int, required=True, help="Target Point ID")
    parser.add_argument("--token", type=str, required=True, help="Augos API Bearer Token")
    parser.add_argument("--out", type=str, default="live_report.json", help="Output JSON path")
    
    args = parser.parse_args()
    
    reporter = AugosLiveReporter(args.token)
    data = reporter.generate_site_report(args.point)
    
    with open(args.out, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n[OK] Report saved to {args.out}")
