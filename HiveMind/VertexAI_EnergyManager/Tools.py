import requests
import json
import datetime
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

# Constants
API_BASE_URL = "https://live.augos.io/api/v1"

def get_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def get_site_details(point_id: int, token: str) -> Dict[str, Any]:
    """
    Retrieves the metadata and hierarchy for a specific site or point.
    """
    url = f"{API_BASE_URL}/measurement/points/point"
    try:
        resp = requests.get(url, params={"pointId": point_id}, headers=get_headers(token), timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def resolve_site_id(search_term: str, token: str) -> List[Dict[str, Any]]:
    """
    Searches for a site or point ID based on a partial name match (e.g., "Westin").
    Returns a list of matching sites with their IDs and Names.
    """
    url = f"{API_BASE_URL}/measurement/points/list"
    try:
        # Fetch all points/sites (or a manageable subset)
        # Note: In a real scenario, we might pass ?filter=... if the API supports it.
        # Here we fetch and filter in-memory for the agent.
        resp = requests.get(url, headers=get_headers(token), timeout=20)
        resp.raise_for_status()
        
        all_points = resp.json()
        matches = []
        
        term = search_term.lower()
        if isinstance(all_points, list):
            for p in all_points:
                # Check Description, Name, or any other label field
                desc = p.get('Description', '').lower()
                name = p.get('Name', '').lower()
                
                if term in desc or term in name:
                    matches.append({
                        "PointID": p.get('PointID'),
                        "Name": p.get('Description') or p.get('Name'),
                        "IsSite": p.get('IsSite', False)
                    })
        
        return matches[:5] # Return top 5 matches
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]


def get_financial_summary(point_id: int, token: str) -> Dict[str, Any]:
    """
    Fetches the latest cost breakdown and invoice verification data.
    """
    now = datetime.datetime.utcnow()
    start = (now - datetime.timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%SZ") # Last 2 months
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Cost Breakdown
    url_cost = f"{API_BASE_URL}/cost-breakdown"
    costs = {}
    try:
        resp = requests.get(url_cost, params={"pointId": point_id, "startDateUTC": start, "endDateUTC": end}, headers=get_headers(token), timeout=20)
        if resp.ok:
            costs = resp.json()
    except:
        pass

    # Invoices
    url_inv = f"{API_BASE_URL}/bills-verification/bill-list"
    invoices = []
    try:
        resp = requests.get(url_inv, params={"pointId": point_id, "startDateUTC": start, "endDateUTC": end}, headers=get_headers(token), timeout=20)
        if resp.ok:
            invoices = resp.json()
    except:
        pass
        
    return {
        "cost_summary": costs,
        "recent_invoices": invoices
    }

def get_power_factor_report(point_id: int, token: str) -> Dict[str, Any]:
    """
    Retrieves Power Factor and Demand peaks for the last 12 months.
    """
    now = datetime.datetime.utcnow()
    start = (now - datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    url = f"{API_BASE_URL}/power-factor-demand"
    try:
        resp = requests.get(url, params={"pointId": point_id, "startDateUTC": start, "endDateUTC": end}, headers=get_headers(token), timeout=20)
        resp.raise_for_status()
        data = resp.json()
        
        # Simple Analysis
        avg_pf = 0
        if isinstance(data, list) and len(data) > 0:
            pfs = [d.get('PFAtPeak', 0) for d in data if d.get('PFAtPeak') is not None]
            if pfs:
                avg_pf = sum(pfs) / len(pfs)
                
        return {
            "data_points": len(data),
            "average_power_factor": round(avg_pf, 3),
            "status": "Good" if avg_pf > 0.95 else "Warning - Low PF",
            "raw_data": data
        }
    except Exception as e:
        return {"error": str(e)}

def analyze_phase_interval_data(point_id: int, token: str, days: int = 7) -> Dict[str, Any]:
    """
    Downloads per-phase interval data (Currents A/B/C) to analyze load balancing.
    Uses '/api/v1/power-factor-demand/download-performance-table' or equivalent export.
    NOTE: Simulated endpoint logic for 'download' as data handling in chat is text-based.
    """
    now = datetime.datetime.utcnow()
    start = (now - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # We define the request for detailed interval data
    # In a real scenario, this might need to POST to a download endpoint and parse CSV
    # For this function, we assume a JSON-compatible endpoint exists or we mock the logic
    # based on what we know of the API structures.
    
    # SIMULATION: Because we don't have the definitive 'per-phase-interval' GET endpoint exposed in Swagger
    # we will treat this as a placeholder wrapper that the user can direct the Agent to use
    # once the specific 'technical analysis' endpoint is confirmed.
    
    return {
        "analysis_period_days": days,
        "status": "Function Ready",
        "message": "To implement true per-phase analysis, map this function to the 'Technical Analysis' graph API endpoint.",
        "simulated_insight": "If data were present, we would calculate (PhaseA_Amps - PhaseB_Amps) / Average_Amps to determine imbalance %."
    }
