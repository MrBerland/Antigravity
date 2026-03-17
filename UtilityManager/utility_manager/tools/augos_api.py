"""
Augos API Tools — One & Only Cape Town (Point ID: 8323)
=========================================================
Covers all 13 Utilities & Services endpoints.
Authentication handled by auth_manager (session cookie, cached, auto-refreshed).
Base URL: https://live.augos.io/api/v1
"""

import datetime
import logging
from typing import Any, Dict, Optional

import requests

from .auth_manager import get_headers, invalidate_token

log = logging.getLogger(__name__)
_API_BASE = "https://live.augos.io/api/v1"


# ─── Helpers ────────────────────────────────────────────────────────────────

def _iso(dt: datetime.datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _date_range(days: int):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=days)
    return _iso(start), _iso(end)


def _months_range(months: int):
    return _date_range(months * 30)


def _get(endpoint: str, params: Dict = None) -> Any:
    url = f"{_API_BASE}/{endpoint}"
    try:
        resp = requests.get(url, params=params, headers=get_headers(), timeout=30)
        if resp.status_code == 401:
            log.warning("401 — invalidating token and retrying once")
            invalidate_token()
            resp = requests.get(url, params=params, headers=get_headers(), timeout=30)
        if resp.status_code == 403:
            return {"error": "403 Forbidden — check AUGOS_EMAIL/AUGOS_PASSWORD in .env"}
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc), "endpoint": endpoint}


def _consumption(point_id: int, product_type_id: int, days: int) -> Any:
    start, end = _date_range(days)
    return _get("consumption-breakdown", {
        "pointID": point_id,
        "startDateUTC": start,
        "endDateUTC": end,
        "productTypeID": product_type_id,
    })


def _try_product_ids(point_id: int, candidate_ids: list, days: int):
    """Try a list of product type IDs and return the first one that returns data."""
    for pid in candidate_ids:
        data = _consumption(point_id, pid, days)
        if "error" not in data and data:
            return pid, data
    return None, None


# ─── Site Discovery ─────────────────────────────────────────────────────────

def resolve_site(search_term: str) -> Dict[str, Any]:
    """
    Search for a hotel or measurement point by name and return its Point ID.

    Use when a site name is given without a numeric Point ID.
    Returns up to 5 matching sites with IDs and site flags.

    Args:
        search_term: Partial or full site name (e.g. 'One Only', 'Royal Atlantis')

    Returns:
        Dictionary with 'matches' list each containing PointID, Name, IsSite.
    """
    result = _get("measurement/points/list", {"search": search_term, "limit": 50})
    if isinstance(result, dict) and "error" in result:
        return result

    items = result.get("data", result) if isinstance(result, dict) else result
    if not isinstance(items, list):
        items = []

    term = search_term.lower()
    matches = []
    for p in items:
        desc = str(p.get("Description", "")).lower()
        name = str(p.get("Name", "")).lower()
        full = str(p.get("fullDescription", "")).lower()
        if term in desc or term in name or term in full:
            matches.append({
                "PointID": p.get("PointID") or p.get("pointID"),
                "Name": p.get("Description") or p.get("Name") or p.get("fullDescription"),
                "IsSite": p.get("IsSite", False),
            })

    return {"search_term": search_term, "matches_found": len(matches[:5]), "matches": matches[:5]}


def get_site_overview(point_id: int) -> Dict[str, Any]:
    """
    Retrieve metadata, hierarchy, and configuration for a site.

    Args:
        point_id: Augos numeric Point ID (e.g. 8323 for One & Only Cape Town)

    Returns:
        Site metadata including name, hierarchy, active meters, and configuration.
    """
    result = _get("measurement/points/point", {"pointID": point_id})
    if isinstance(result, dict) and "error" in result:
        result = _get("measurement/points/point", {"pointId": point_id})
    return result


# ─── Consumption ────────────────────────────────────────────────────────────

def get_electricity_consumption(point_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Retrieve electricity consumption breakdown for the site.

    Returns hierarchical consumption (site total + sub-meters).
    Use for anomaly detection, base load analysis, and cost investigation.

    Args:
        point_id: Augos Point ID (default: 8323)
        days: Lookback window — 7 (operational), 30 (billing), 90 (seasonal), 730 (2yr)

    Returns:
        Electricity consumption data with totals and sub-point breakdown.
    """
    start, end = _date_range(days)
    data = _consumption(point_id, 2, days)
    return {
        "utility": "electricity", "unit": "kWh",
        "point_id": point_id,
        "period": {"start": start, "end": end, "days": days},
        "data": data,
    }


def get_water_consumption(point_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Retrieve water consumption breakdown for the site.

    Critical for leak detection (overnight base load), EarthCheck potable
    water KPI reporting, and occupancy correlation.

    Args:
        point_id: Augos Point ID
        days: Lookback window in days

    Returns:
        Water consumption data with product_type_id discovered, totals, and sub-meter breakdown.
    """
    start, end = _date_range(days)
    pid, data = _try_product_ids(point_id, [3, 4, 5, 6], days)
    if pid is None:
        return {
            "utility": "water", "error": "No active water product type found. "
            "Check Augos portal for the correct productTypeID and update config/product_types.yaml",
            "tried_ids": [3, 4, 5, 6],
        }
    return {
        "utility": "water", "unit": "kL",
        "product_type_id": pid,
        "point_id": point_id,
        "period": {"start": start, "end": end, "days": days},
        "data": data,
    }


def get_gas_consumption(point_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Retrieve gas consumption breakdown for the site.

    Use for kitchen efficiency, overnight base load monitoring (gas outside
    kitchen hours = waste), and Scope 1 carbon calculations.

    Args:
        point_id: Augos Point ID
        days: Lookback window in days

    Returns:
        Gas consumption data with product_type_id discovered, totals, and sub-meter breakdown.
    """
    start, end = _date_range(days)
    pid, data = _try_product_ids(point_id, [7, 8, 9, 10, 11], days)
    if pid is None:
        return {
            "utility": "gas", "error": "No active gas product type found. "
            "Check Augos portal for the correct productTypeID and update config/product_types.yaml",
            "tried_ids": [7, 8, 9, 10, 11],
        }
    return {
        "utility": "gas", "unit": "m3",
        "product_type_id": pid,
        "point_id": point_id,
        "period": {"start": start, "end": end, "days": days},
        "data": data,
    }


def get_all_utility_consumption(point_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Retrieve consumption for ALL utilities (electricity, water, gas) in one call.

    Use for executive summaries, cross-utility anomaly detection, and portfolio overviews.

    Args:
        point_id: Augos Point ID
        days: Lookback window in days

    Returns:
        Combined consumption data with electricity, water, and gas sections.
    """
    return {
        "point_id": point_id, "days": days,
        "electricity": get_electricity_consumption(point_id, days),
        "water": get_water_consumption(point_id, days),
        "gas": get_gas_consumption(point_id, days),
    }


# ─── Financial ──────────────────────────────────────────────────────────────

def get_cost_analysis(point_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Fetch full electricity cost breakdown with tariff line items and totals in ZAR.

    Returns tariff metadata (scheme, authority), line items (peak/standard/off-peak
    consumption, demand, network charges), rates (ZAR/kWh), and totals.
    Use for billing verification, ToU analysis, and budget reporting.

    Args:
        point_id: Augos Point ID
        days: Billing period in days

    Returns:
        Cost breakdown dict with tariff metadata and itemised ZAR charges.
    """
    start, end = _date_range(days)
    data = _get("cost-breakdown", {
        "pointID": point_id, "startDateUTC": start,
        "endDateUTC": end, "productTypeID": 2, "billing": 0,
    })
    return {"point_id": point_id, "period": {"start": start, "end": end, "days": days}, "cost_data": data}


def get_bill_verification(point_id: int, months: int = 3) -> Dict[str, Any]:
    """
    Compare Augos-calculated consumption against utility-billed amounts.

    Identifies billing discrepancies, overbilling, and invoice accuracy.

    Args:
        point_id: Augos Point ID
        months: Months of billing history to review

    Returns:
        Bill verification data with calculated-vs-billed comparison records.
    """
    start, end = _months_range(months)
    return {
        "point_id": point_id, "period_months": months,
        "data": _get("bill-verification", {
            "pointID": point_id, "startDateUTC": start,
            "endDateUTC": end, "productTypeID": 2,
        })
    }


def get_cost_allocation(point_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Retrieve cost allocation across sub-measurement points (cost centres).

    Shows cost distribution per department or meter.

    Args:
        point_id: Augos Point ID
        days: Period to analyse

    Returns:
        Cost allocation per sub-point with ZAR values and percentages.
    """
    start, end = _date_range(days)
    return {
        "point_id": point_id, "period_days": days,
        "data": _get("cost-allocation", {
            "pointID": point_id, "startDateUTC": start,
            "endDateUTC": end, "productTypeID": 2,
        })
    }


def get_tariff_comparison(point_id: int) -> Dict[str, Any]:
    """
    Compare the current tariff against all available alternative tariff schemes.

    The hotel is currently on City of Cape Town Large Power User (MV) TOU.
    This shows what alternative tariffs would cost and identifies ZAR savings.

    Args:
        point_id: Augos Point ID

    Returns:
        Comparative cost analysis across available tariff alternatives.
    """
    return {"point_id": point_id, "data": _get("electricity/tariff-comparison", {"pointID": point_id})}


# ─── Technical / Operational ────────────────────────────────────────────────

def get_power_factor(point_id: int, months: int = 12) -> Dict[str, Any]:
    """
    Retrieve Power Factor and Peak Demand analysis.

    PF < 0.95 = potential CoCT penalties. PF < 0.90 = P1 Critical — immediate action.
    Returns monthly PF trend, demand peaks, and reactive power data.

    Args:
        point_id: Augos Point ID
        months: Months of PF history (default 12 for full seasonal cycle)

    Returns:
        PF trend, average, minimum, peak demand (kVA), and penalty risk assessment.
    """
    start, end = _months_range(months)
    data = _get("power-factor-demand", {"pointID": point_id, "startDateUTC": start, "endDateUTC": end})

    if isinstance(data, dict) and "error" in data:
        return data

    pfs = [d.get("PFAtPeak", 0) for d in (data if isinstance(data, list) else []) if d.get("PFAtPeak")]
    demands = [d.get("MaxDemandKVA", 0) for d in (data if isinstance(data, list) else []) if d.get("MaxDemandKVA")]

    avg_pf = sum(pfs) / len(pfs) if pfs else 0
    min_pf = min(pfs) if pfs else None
    max_demand = max(demands) if demands else None

    status = "Good" if avg_pf >= 0.95 else ("Warning" if avg_pf >= 0.92 else "Critical")
    reco = {
        "Good": "Power factor is healthy. No action required.",
        "Warning": "PF below 0.95 — CoCT penalties may be accruing. Inspect capacitor banks.",
        "Critical": "PF critically low (<0.92) — utility penalties being incurred. Immediate capacitor bank review required.",
    }[status]

    return {
        "point_id": point_id, "period": {"start": start, "end": end, "months": months},
        "data_points": len(data) if isinstance(data, list) else 0,
        "average_power_factor": round(avg_pf, 3),
        "minimum_power_factor": round(min_pf, 3) if min_pf else None,
        "max_demand_kva": round(max_demand, 2) if max_demand else None,
        "status": status, "recommendation": reco,
        "raw_data": data[:12] if isinstance(data, list) else data,
    }


def get_time_of_use(point_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Retrieve Time-of-Use consumption breakdown (Peak / Standard / Off-Peak).

    Shows what percentage of electricity is consumed in each tariff period.
    Use to quantify ToU optimisation opportunities and load-shifting savings.

    Args:
        point_id: Augos Point ID
        days: Period to analyse

    Returns:
        ToU consumption split with kWh and ZAR cost per period.
    """
    start, end = _date_range(days)
    return {
        "point_id": point_id, "period": {"start": start, "end": end, "days": days},
        "data": _get("electricity/time-of-use", {"pointID": point_id, "startDateUTC": start, "endDateUTC": end})
    }


def get_technical_analysis(point_id: int, days: int = 7) -> Dict[str, Any]:
    """
    Retrieve technical interval data for detailed engineering analysis.

    Returns demand time-series and per-phase data (where available) for
    phase imbalance detection, outage identification, and load profiling.

    Args:
        point_id: Augos Point ID
        days: Period to retrieve — keep short (7 days) to avoid large payloads

    Returns:
        Technical time-series demand data and meter list.
    """
    start, end = _date_range(days)
    return {
        "point_id": point_id, "period": {"start": start, "end": end, "days": days},
        "data": _get("technical-analysis", {
            "pointID": point_id, "startDateUTC": start, "endDateUTC": end, "productTypeID": 2,
        })
    }


def get_dashboard(point_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Retrieve dashboard KPI summary data for the site.

    Returns aggregated KPIs for consumption, cost, and demand — ideal for
    executive briefings and overall site health checks.

    Args:
        point_id: Augos Point ID
        days: Period to analyse

    Returns:
        Dashboard KPI data including consumption, cost, and demand summary.
    """
    start, end = _date_range(days)
    return {
        "point_id": point_id, "period": {"start": start, "end": end, "days": days},
        "data": _get("dashboard", {
            "pointID": point_id, "startDateUTC": start,
            "endDateUTC": end, "productTypeID": 2,
        })
    }


def get_live_curtailment_status(point_id: int) -> Dict[str, Any]:
    """
    Retrieve real-time load curtailment compliance status.

    Shows whether the site is complying with its Curtailment Base Load (CBL)
    and current curtailment stage. Use during high-demand alerts.

    Args:
        point_id: Augos Point ID

    Returns:
        Real-time curtailment compliance data with stage information.
    """
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    return {
        "point_id": point_id, "date": today,
        "data": _get("load-curtailment/get-load-curtailment", {
            "pointID": point_id, "date": today, "offset": -120,
        })
    }


def get_sensor_readings(point_id: int, days: int = 7) -> Dict[str, Any]:
    """
    Retrieve Sensing & Monitoring sensor readings for the site.

    Returns environmental sensor data (temperature, humidity, pressure, etc.)
    connected via the Augos S&M module.

    Args:
        point_id: Augos Point ID
        days: Period to retrieve

    Returns:
        Sensor readings from the S&M module for the specified period.
    """
    start, end = _date_range(days)
    return {
        "point_id": point_id, "period": {"start": start, "end": end, "days": days},
        "data": _get("charting", {
            "pointID": point_id, "startDateUTC": start, "endDateUTC": end,
            "resolution": "halfhour",
        })
    }
