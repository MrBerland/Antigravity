"""
Energy Manager Tools

This module contains all the tools (functions) that the Energy Manager agent
can use to interact with the Augos Energy Platform API.

Authentication: Uses full cookie string including JWT token.
"""
import os
import requests
import datetime
from typing import Dict, Any, List

# API Configuration
API_BASE_URL = "https://live.augos.io/api/v1"

def _get_cookies() -> str:
    """Retrieve the Augos cookies from environment."""
    cookies = os.environ.get("AUGOS_COOKIES", "")
    if not cookies:
        raise ValueError("AUGOS_COOKIES environment variable is not set")
    return cookies

def _get_headers() -> Dict[str, str]:
    """Build request headers for the Augos API."""
    return {
        "Accept": "application/json, text/plain, */*",
        "Cookie": _get_cookies(),
        "Referer": "https://live.augos.io/"
    }

def _make_request(endpoint: str, params: Dict = None) -> Dict:
    """Make an authenticated request to the Augos API."""
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        resp = requests.get(url, params=params, headers=_get_headers(), timeout=30)
        
        if resp.status_code == 403:
            return {
                "error": "Authentication failed (403 Forbidden)",
                "help": "Your session may have expired. Please refresh cookies:",
                "steps": [
                    "1. Log in to https://live.augos.io",
                    "2. Open DevTools (F12) → Network tab",
                    "3. Click any API request to /api/v1/",
                    "4. Copy the entire Cookie header value",
                    "5. Update AUGOS_COOKIES in your .env file"
                ]
            }
        
        if resp.status_code == 401:
            return {
                "error": "Session expired (401 Unauthorized)",
                "help": "Please log in again to refresh your session"
            }
        
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}


def resolve_site_id(search_term: str) -> Dict[str, Any]:
    """
    Search for a site by name and return matching Point IDs.
    
    Use this tool when the user mentions a site name (like "The Westin" or "V&A Waterfront")
    but doesn't provide a numeric Point ID. Returns up to 5 matching sites.
    
    Args:
        search_term: Partial or full site name to search for (e.g., "Westin", "Cape Town")
    
    Returns:
        Dictionary with matches containing PointID, Name, and IsSite flag
    """
    # Try the search endpoint
    result = _make_request("measurement/points/list", {
        "search": search_term,
        "limit": 50
    })
    
    if "error" in result:
        return result
    
    matches = []
    
    # Handle paginated response
    if isinstance(result, dict) and "data" in result:
        items = result.get("data", [])
    elif isinstance(result, list):
        items = result
    else:
        items = []
    
    term = search_term.lower()
    for p in items:
        desc = str(p.get('Description', '')).lower()
        name = str(p.get('Name', '')).lower()
        full = str(p.get('fullDescription', '')).lower()
        
        if term in desc or term in name or term in full:
            matches.append({
                "PointID": p.get('PointID') or p.get('pointID'),
                "Name": p.get('Description') or p.get('Name') or p.get('fullDescription'),
                "IsSite": p.get('IsSite', False)
            })
    
    if not matches:
        # Provide helpful guidance when no results found
        return {
            "message": f"No sites found matching '{search_term}'",
            "matches": [],
            "suggestions": [
                "Check the spelling of the site name",
                "Try a shorter search term (e.g., just 'Finlar' instead of 'Finlar Stikland')",
                "If you know the Point ID, you can use it directly with the consumption or report tools",
                "Common sites: 3 The Terrace (45829614), The Westin, V&A Waterfront"
            ],
            "tip": "If you have access to the Augos portal, you can find Point IDs in the URL when viewing a site."
        }
    
    return {"message": f"Found {len(matches[:5])} matches", "matches": matches[:5]}


def get_site_details(point_id: int) -> Dict[str, Any]:
    """
    Retrieve metadata and hierarchy for a specific site or measurement point.
    
    Use this tool to get basic information about a site including its name,
    location in the hierarchy, and configuration details.
    
    Args:
        point_id: The numeric Point ID of the site (e.g., 45829614)
    
    Returns:
        Dictionary containing site metadata, hierarchy, and configuration
    """
    # Try with pointID (uppercase ID)
    result = _make_request("measurement/points/point", {"pointID": point_id})
    
    if "error" in result and "pointID" in str(result):
        # Try alternate parameter name
        result = _make_request("measurement/points/point", {"pointId": point_id})
    
    return result


def get_financial_summary(point_id: int, months: int = 2) -> Dict[str, Any]:
    """
    Fetch cost breakdown and invoice data for a site.
    
    Use this tool to get financial information including utility costs,
    bill verification status, and recent invoices.
    
    Args:
        point_id: The numeric Point ID of the site
        months: Number of months of data to retrieve (default: 2)
    
    Returns:
        Dictionary with cost_summary and recent_invoices
    """
    now = datetime.datetime.utcnow()
    start = (now - datetime.timedelta(days=months * 30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    result = {
        "period": {"start": start, "end": end},
        "cost_summary": None,
        "recent_invoices": []
    }
    
    # Cost Breakdown
    cost_data = _make_request("cost-breakdown", {
        "pointID": point_id,
        "startDateUTC": start,
        "endDateUTC": end
    })
    
    if "error" not in cost_data:
        result["cost_summary"] = cost_data
    else:
        result["cost_error"] = cost_data.get("error")
    
    # Invoices
    invoice_data = _make_request("bills-verification/bill-list", {
        "pointID": point_id,
        "startDateUTC": start,
        "endDateUTC": end
    })
    
    if "error" not in invoice_data:
        result["recent_invoices"] = invoice_data
    else:
        result["invoice_error"] = invoice_data.get("error")
    
    return result


def get_power_factor_report(point_id: int, months: int = 12) -> Dict[str, Any]:
    """
    Retrieve Power Factor and Demand analysis for a site.
    
    Use this tool to analyze power factor trends and identify penalty risks.
    A power factor below 0.95 typically indicates potential utility penalties
    and suggests reviewing capacitor banks.
    
    Args:
        point_id: The numeric Point ID of the site
        months: Number of months of historical data (default: 12)
    
    Returns:
        Dictionary with average PF, status assessment, and raw data points
    """
    now = datetime.datetime.utcnow()
    start = (now - datetime.timedelta(days=months * 30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    data = _make_request("power-factor-demand", {
        "pointID": point_id,
        "startDateUTC": start,
        "endDateUTC": end
    })
    
    if "error" in data:
        return data
    
    # Analysis
    avg_pf = 0
    min_pf = None
    max_demand = None
    
    if isinstance(data, list) and len(data) > 0:
        pfs = [d.get('PFAtPeak', 0) for d in data if d.get('PFAtPeak') is not None]
        demands = [d.get('MaxDemandKVA', 0) for d in data if d.get('MaxDemandKVA') is not None]
        
        if pfs:
            avg_pf = sum(pfs) / len(pfs)
            min_pf = min(pfs)
        if demands:
            max_demand = max(demands)
    
    # Determine status and recommendations
    if avg_pf > 0.95:
        status = "Good"
        recommendation = "Power factor is healthy. No action required."
    elif avg_pf > 0.90:
        status = "Warning"
        recommendation = "Power factor slightly low. Consider capacitor bank inspection."
    else:
        status = "Critical"
        recommendation = "Power factor critically low. Immediate capacitor bank review recommended. Likely incurring utility penalties."
            
    return {
        "period": {"start": start, "end": end},
        "data_points": len(data) if isinstance(data, list) else 0,
        "average_power_factor": round(avg_pf, 3),
        "minimum_power_factor": round(min_pf, 3) if min_pf else None,
        "max_demand_kva": round(max_demand, 2) if max_demand else None,
        "status": status,
        "recommendation": recommendation,
        "raw_data": data[:10] if isinstance(data, list) else data
    }


def get_consumption_summary(point_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Get consumption data summary for a site over a specified period.
    
    Use this tool to analyze energy consumption patterns, identify
    anomalies, and check if the site is reporting data correctly.
    
    Args:
        point_id: The numeric Point ID of the site
        days: Number of days of data to retrieve (default: 30)
    
    Returns:
        Dictionary with consumption totals and telemetry status
    """
    now = datetime.datetime.utcnow()
    start = (now - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    data = _make_request("consumption-breakdown", {
        "pointID": point_id,
        "startDateUTC": start,
        "endDateUTC": end,
        "productTypeID": 2  # Electricity
    })
    
    if "error" in data:
        return data
    
    # Parse consumption data
    total_consumption = 0
    site_name = None
    
    if isinstance(data, list) and len(data) > 0:
        # First item in first list is usually the site total
        if isinstance(data[0], list) and len(data[0]) > 0:
            site_info = data[0][0]
            total_consumption = site_info.get('consumption', 0)
            site_name = site_info.get('fullDescription')
    
    has_data = total_consumption > 0
    
    return {
        "site_name": site_name,
        "period": {"start": start, "end": end, "days": days},
        "telemetry_status": "Online" if has_data else "No Data",
        "total_consumption_kwh": round(total_consumption, 2),
        "consumption_breakdown": data
    }


def generate_site_report(point_id: int) -> Dict[str, Any]:
    """
    Generate a comprehensive site report combining all available data.
    
    This is a high-level tool that aggregates site details, financial summary,
    power factor analysis, and consumption data into a single report.
    Use this when the user asks for a "site report" or "full analysis".
    
    Args:
        point_id: The numeric Point ID of the site
    
    Returns:
        Comprehensive dictionary with all site metrics and assessments
    """
    report = {
        "report_generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "point_id": point_id,
        "sections": {}
    }
    
    # 1. Site Details
    report["sections"]["site_details"] = get_site_details(point_id)
    
    # 2. Consumption (last 30 days) - do this first to get site name
    consumption = get_consumption_summary(point_id, days=30)
    report["sections"]["consumption"] = consumption
    report["site_name"] = consumption.get("site_name", f"Site {point_id}")
    
    # 3. Financial Summary (last 2 months)
    report["sections"]["financial"] = get_financial_summary(point_id, months=2)
    
    # 4. Power Factor (last 12 months)
    report["sections"]["power_factor"] = get_power_factor_report(point_id, months=12)
    
    # 5. Overall Assessment
    pf_status = report["sections"]["power_factor"].get("status", "Unknown")
    telemetry = consumption.get("telemetry_status", "Unknown")
    
    if pf_status == "Good" and telemetry == "Online":
        overall = "Healthy"
    elif "error" in str(report["sections"]["power_factor"]) or telemetry == "No Data":
        overall = "Needs Attention - Data Issues"
    else:
        overall = "Needs Review"
    
    report["overall_status"] = overall
    
    return report
