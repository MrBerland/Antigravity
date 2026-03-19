"""
KPI Engine — Six Strategic Energy Performance Indicators
=========================================================
Computes, stores, and trends the platform's six core KPIs:

  1. Energy Index       — kWh per Cooling Degree Day (climate-normalised efficiency)
  2. Cost Index         — ZAR per CDD (financial efficiency)
  3. Demand Utilisation — Peak kVA as % of NMD
  4. Power Quality Score — Weighted PF across all independent PFC systems
  5. Load Shift Index   — % of shiftable load operating in off-peak window
  6. Asset Compliance Score — % of mandatory assessments currently up-to-date

These six appear at the top of every report, for every persona, every period.
Their definition never changes — consistency is the product.
"""

import logging
import os
from datetime import datetime, timedelta, date
from typing import Any, Dict, List, Optional, Tuple

import requests

from .auth_manager import get_headers
from .cdd_engine import get_monthly_cdd_series, CDD_BASE

log = logging.getLogger(__name__)

_API_BASE = "https://live.augos.io/api/v1"

# Site constants — read from env or fall back to One & Only CT defaults
_LAT         = float(os.getenv("SITE_LAT", "-33.9249"))
_LON         = float(os.getenv("SITE_LON", "18.4241"))
_SITE_ID     = int(os.getenv("AUGOS_SITE_POINT_ID", "8323"))
_NMD_KVA     = float(os.getenv("CONTRACTED_DEMAND_KVA") or "0")      # 0 = unknown
_PFC_POINTS  = [
    {"id": 8324, "label": "Main Switch 1 (PFC-A)", "weight": 0.56},
    {"id": 8336, "label": "Main Switch 2 (PFC-B)", "weight": 0.44},
]

# Tariff type IDs and rates in Augos billing
_TARIFF_PEAK     = 36
_TARIFF_STANDARD = 56
_TARIFF_OFFPEAK  = 37
# Known CoCT TOU rates (ZAR/kWh) — used to back-calculate kWh from cost
_RATE_PEAK       = 3.3396
_RATE_STANDARD   = 2.1708
_RATE_OFFPEAK    = 1.7563
# Minimum monthly CDD for a meaningful Energy Index comparison
_MIN_CDD_FOR_EI  = 30


# ─── Billing history ─────────────────────────────────────────────────────────

def _fetch_billing_history(months: int = 36) -> List[Dict]:
    """
    Pull monthly billing summary (bucket 6) from Augos.
    Returns list of {month_key, kwh, cost, max_demand_kva}.
    """
    end   = datetime.utcnow()
    start = end - timedelta(days=months * 31)
    fmt   = "%Y-%m-%dT%H:%M:%SZ"

    r = requests.get(f"{_API_BASE}/cost-breakdown", params={
        "pointID": _SITE_ID,
        "startDateUTC": start.strftime(fmt),
        "endDateUTC":   end.strftime(fmt),
        "productTypeID": 2,
        "billing": 0,
    }, headers=get_headers(), timeout=30)

    data = r.json() if r.ok else []
    bucket6 = data[6] if isinstance(data, list) and len(data) > 6 else []
    bucket2 = data[2] if isinstance(data, list) and len(data) > 2 else []

    # Monthly summary from bucket 6
    monthly: Dict[str, Dict] = {}
    for row in bucket6:
        if not isinstance(row, dict) or not row.get("monthDescription"):
            continue
        kwh  = row.get("consumption", 0) or 0
        cost = row.get("cost", 0) or 0
        dem  = row.get("maxDemand", 0) or 0
        if kwh <= 0 and cost <= 0:
            continue
        # Convert Augos "Jan 26" → "2026-01"
        key = _month_desc_to_key(row["monthDescription"])
        if key:
            monthly[key] = {"kwh": kwh, "cost": cost, "max_demand_kva": dem}

    # Off-peak kWh from bucket 2 — consumption field is None, back-calculate from cost
    offpeak_by_month: Dict[str, float] = {}
    total_by_month:   Dict[str, float] = {}
    rate_map = {
        _TARIFF_PEAK:     _RATE_PEAK,
        _TARIFF_STANDARD: _RATE_STANDARD,
        _TARIFF_OFFPEAK:  _RATE_OFFPEAK,
    }
    for row in bucket2:
        if not isinstance(row, dict):
            continue
        tid  = row.get("tariffTypeID")
        desc = row.get("monthDescription", "")
        cost = row.get("cost", 0) or 0
        rate = rate_map.get(tid)
        if not rate or cost <= 0:
            continue
        key  = _month_desc_to_key(desc)
        if not key:
            continue
        kwh_est = cost / rate
        total_by_month[key] = total_by_month.get(key, 0) + kwh_est
        if tid == _TARIFF_OFFPEAK:
            offpeak_by_month[key] = offpeak_by_month.get(key, 0) + kwh_est

    # Merge off-peak data
    for key in monthly:
        op  = offpeak_by_month.get(key, 0)
        tot = total_by_month.get(key, 0) or monthly[key]["kwh"]
        monthly[key]["offpeak_kwh"] = op
        monthly[key]["total_kwh_tou"] = tot

    return monthly


def _fetch_pf_history(months: int = 14) -> Dict[str, Dict]:
    """
    Fetch monthly PF data for all PFC points.
    Returns {pfc_label: {"YYYY-MM": pf_value}}.
    """
    end   = datetime.utcnow()
    start = end - timedelta(days=months * 31)
    fmt   = "%Y-%m-%dT%H:%M:%SZ"
    result = {}

    for pfc in _PFC_POINTS:
        r = requests.get(f"{_API_BASE}/power-factor-demand", params={
            "pointID":      pfc["id"],
            "startDateUTC": start.strftime(fmt),
            "endDateUTC":   end.strftime(fmt),
        }, headers=get_headers(), timeout=30)
        details = r.json().get("details", []) if r.ok else []
        pf_row  = next((d for d in details if d.get("itemsDescription") == "actualPf"), {})
        skip    = {"index", "pointID", "point", "parentID", "itemsDescription", "total"}
        monthly_pf = {}
        for k, v in pf_row.items():
            if k not in skip and v is not None:
                key = _month_desc_to_key(k)
                if key:
                    monthly_pf[key] = v
        result[pfc["label"]] = {"weight": pfc["weight"], "monthly": monthly_pf}

    return result


# ─── Compliance Calendar ──────────────────────────────────────────────────────

def _score_compliance(profile: Dict) -> Dict:
    """
    Score the asset compliance calendar.
    Returns compliance score (0–100) and list of overdue/due items.
    """
    calendar = profile.get("compliance_calendar", {})
    items   = []
    today   = date.today()

    checks = [
        ("certificate_of_compliance",  "Certificate of Compliance",  365,  "Legal requirement. Immediately flag if expired."),
        ("thermographic_scan",          "Thermographic Scan",         365,  "Insurance requirement. Annual recommended."),
        ("pf_survey_switch_1",          "PF Survey — Main Switch 1",  365,  "Augos assessment. Priority: seasonal degradation."),
        ("pf_survey_switch_2",          "PF Survey — Main Switch 2",  730,  "Augos assessment. Reference system, biennial."),
        ("transformer_oil_test",        "Transformer Oil Test",        730,  "Manufacturer requirement. Biennial."),
        ("earth_continuity_test",       "Earth Continuity Test",       365,  "Safety requirement. Annual."),
    ]

    scored = 0
    total  = len(checks)
    overdue, due_soon, current = [], [], []

    for field, label, max_days, rationale in checks:
        entry      = calendar.get(field, {})
        last_str   = entry.get("last_completed") or entry.get("last_issued")
        if not last_str:
            days_since = None
            overdue.append({"item": label, "status": "Never recorded", "rationale": rationale})
            continue

        try:
            last_date  = datetime.strptime(last_str, "%Y-%m-%d").date()
            days_since = (today - last_date).days
        except (ValueError, TypeError):
            days_since = None
            overdue.append({"item": label, "status": "Invalid date", "rationale": rationale})
            continue

        if days_since > max_days:
            overdue.append({
                "item": label,
                "days_overdue": days_since - max_days,
                "last_completed": last_str,
                "rationale": rationale,
            })
        elif days_since > max_days * 0.8:
            due_soon.append({
                "item": label,
                "days_remaining": max_days - days_since,
                "last_completed": last_str,
            })
            scored += 0.5
        else:
            current.append({"item": label, "last_completed": last_str})
            scored += 1.0

    score = round((scored / total) * 100) if total > 0 else 0

    return {
        "score": score,
        "total_items": total,
        "overdue": overdue,
        "due_soon": due_soon,
        "current": current,
    }


# ─── Main KPI computation ────────────────────────────────────────────────────

def compute_kpis(
    months: int = 3,
    site_profile: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Compute all six strategic KPIs for the most recent N months.

    Args:
        months: How many months to compute (for trending — uses last 3 by default)
        site_profile: Site profile dict (from config/site_profile.yaml) for compliance scoring

    Returns:
        {
          "computed_at": str,
          "months": ["YYYY-MM", ...],
          "kpis": {
            "energy_index": {"current": float, "prior": float, "ly": float, "trend": str},
            "cost_index":   {...},
            "demand_utilisation": {...},
            "power_quality_score": {...},
            "load_shift_index": {...},
            "asset_compliance_score": {...},
          },
          "monthly_detail": {...},
        }
    """
    log.info("Computing 6 strategic KPIs — %d month window", months)

    # --- Fetch all data ---
    billing  = _fetch_billing_history(months=max(months + 14, 36))
    cdd_data = get_monthly_cdd_series(_LAT, _LON)
    pf_data  = _fetch_pf_history(months=max(months + 3, 14))

    # --- Identify target months (sorted, most recent, CDD > min for EnPI) ---
    all_months = sorted(set(billing) & set(cdd_data), reverse=True)
    if not all_months:
        return {"error": "No months with both billing and weather data available."}

    recent  = all_months[:months]
    # For EnPI trend: only compare against months with CDD > minimum threshold
    # (prevents nonsensical division by near-zero winter CDD)
    all_hi_cdd = [m for m in all_months if cdd_data.get(m, {}).get("cdd", 0) >= _MIN_CDD_FOR_EI]
    prior_m  = [m for m in all_hi_cdd if m not in recent][:months]
    same_ly  = _same_period_last_year(recent)

    monthly_detail = {}
    kpi_series: Dict[str, List] = {
        "energy_index": [], "cost_index": [], "demand_utilisation": [],
        "power_quality_score": [], "load_shift_index": [],
    }

    for m in recent:
        b   = billing.get(m, {})
        cdd = cdd_data.get(m, {}).get("cdd", 0) or 0
        kwh = b.get("kwh", 0) or 0
        cost = b.get("cost", 0) or 0
        dem  = b.get("max_demand_kva", 0) or 0

        # 1. Energy Index
        ei = round(kwh / cdd, 1) if cdd > 0 else None

        # 2. Cost Index
        ci = round(cost / cdd, 0) if cdd > 0 else None

        # 3. Demand Utilisation
        du = round(dem / _NMD_KVA * 100, 1) if _NMD_KVA > 0 else None

        # 4. Power Quality Score — weighted PF across switches
        pf_vals, pf_weights = [], []
        pf_breakdown = {}
        for pfc in _PFC_POINTS:
            label = pfc["label"]
            pf_val = pf_data.get(label, {}).get("monthly", {}).get(m)
            if pf_val and pf_val > 0.5:  # sanity check
                pf_vals.append(pf_val)
                pf_weights.append(pfc["weight"])
                pf_breakdown[label] = round(pf_val, 4)
        if pf_vals:
            weighted_pf = sum(v * w for v, w in zip(pf_vals, pf_weights)) / sum(pf_weights)
            pq = round(weighted_pf * 100, 1)
        else:
            pq = None

        # 5. Load Shift Index
        op_kwh  = b.get("offpeak_kwh", 0) or 0
        tot_kwh = b.get("total_kwh_tou", 0) or kwh
        lsi = round(op_kwh / tot_kwh * 100, 1) if tot_kwh > 0 and op_kwh > 0 else None

        monthly_detail[m] = {
            "kwh": kwh, "cost": cost, "max_demand_kva": dem, "cdd": cdd,
            "energy_index": ei, "cost_index": ci,
            "demand_utilisation": du, "power_quality_score": pq,
            "load_shift_index": lsi,
            "pf_by_switch": pf_breakdown,
        }

        if ei:  kpi_series["energy_index"].append(ei)
        if ci:  kpi_series["cost_index"].append(ci)
        if du is not None: kpi_series["demand_utilisation"].append(du)
        if pq:  kpi_series["power_quality_score"].append(pq)
        if lsi: kpi_series["load_shift_index"].append(lsi)

    # --- Compute prior period and last year for trending ---
    prior_detail = _compute_period_averages(prior_m, billing, cdd_data, pf_data)
    ly_detail    = _compute_period_averages(same_ly, billing, cdd_data, pf_data)

    # --- Compliance score ---
    compliance = _score_compliance(site_profile or {})

    def _avg(lst):
        return round(sum(lst) / len(lst), 1) if lst else None

    def _trend(curr, prev):
        if curr is None or prev is None:
            return "→ No comparison"
        d = curr - prev
        if abs(d) < 0.5:
            return "→ Stable"
        # For EI and CI: lower is better. For DU: lower is better. For PQ, LSI, Compliance: higher is better.
        return f"▲ {abs(d):.1f}" if d > 0 else f"▼ {abs(d):.1f}"

    curr_ei   = _avg(kpi_series["energy_index"])
    curr_ci   = _avg(kpi_series["cost_index"])
    curr_du   = _avg(kpi_series["demand_utilisation"])
    curr_pq   = _avg(kpi_series["power_quality_score"])
    curr_lsi  = _avg(kpi_series["load_shift_index"])

    return {
        "computed_at":   datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "period_months": recent,
        "kpis": {
            "energy_index": {
                "label":       "Energy Index",
                "unit":        "kWh/CDD",
                "description": "Climate-normalised energy efficiency. Lower = better.",
                "current":     curr_ei,
                "prior":       prior_detail.get("energy_index"),
                "last_year":   ly_detail.get("energy_index"),
                "trend_vs_prior": _trend(curr_ei, prior_detail.get("energy_index")),
                "note":        "Decreasing trend = genuine efficiency improvement (weather removed)",
            },
            "cost_index": {
                "label":       "Cost Index",
                "unit":        "R/CDD",
                "description": "Financial efficiency per degree day. Separates tariff from operations.",
                "current":     curr_ci,
                "prior":       prior_detail.get("cost_index"),
                "last_year":   ly_detail.get("cost_index"),
                "trend_vs_prior": _trend(curr_ci, prior_detail.get("cost_index")),
            },
            "demand_utilisation": {
                "label":       "Demand Utilisation",
                "unit":        "% of NMD",
                "description": "Peak kVA as % of Notified Maximum Demand. >95% = risk.",
                "current":     curr_du,
                "prior":       prior_detail.get("demand_utilisation"),
                "last_year":   ly_detail.get("demand_utilisation"),
                "trend_vs_prior": _trend(curr_du, prior_detail.get("demand_utilisation")),
                "nmd_kva":     _NMD_KVA if _NMD_KVA > 0 else "NOT CONFIGURED — add CONTRACTED_DEMAND_KVA to .env",
                "status":      _du_status(curr_du),
            },
            "power_quality_score": {
                "label":       "Power Quality Score",
                "unit":        "PF × 100",
                "description": "Weighted average PF across all PFC systems. >97 = good.",
                "current":     curr_pq,
                "prior":       prior_detail.get("power_quality_score"),
                "last_year":   ly_detail.get("power_quality_score"),
                "trend_vs_prior": _trend(curr_pq, prior_detail.get("power_quality_score")),
                "by_switch":   {m: monthly_detail[m]["pf_by_switch"] for m in recent if m in monthly_detail},
                "status":      _pq_status(curr_pq),
            },
            "load_shift_index": {
                "label":       "Load Shift Index",
                "unit":        "% off-peak",
                "description": "% of TOU-metered energy consumed in off-peak window. Higher = better.",
                "current":     curr_lsi,
                "prior":       prior_detail.get("load_shift_index"),
                "last_year":   ly_detail.get("load_shift_index"),
                "trend_vs_prior": _trend(curr_lsi, prior_detail.get("load_shift_index")),
                "opportunity_zar_monthly": _lsi_opportunity(billing, recent),
            },
            "asset_compliance_score": {
                "label":       "Asset Compliance Score",
                "unit":        "%",
                "description": "% of mandatory assessments currently up-to-date.",
                "current":     compliance["score"],
                "overdue":     compliance["overdue"],
                "due_soon":    compliance["due_soon"],
                "current_items": compliance["current"],
                "status":      "⚠ Action required" if compliance["overdue"] else ("✓ Good" if compliance["score"] >= 80 else "Monitor"),
            },
        },
        "monthly_detail": monthly_detail,
    }


# ─── Status helpers ──────────────────────────────────────────────────────────

def _du_status(du: Optional[float]) -> str:
    if du is None: return "⚠ NMD not configured"
    if du >= 100:  return "🔴 CRITICAL — NMD exceeded"
    if du >= 95:   return "🔴 WARNING — approaching NMD"
    if du >= 85:   return "🟡 WATCH — elevated demand risk"
    return "✓ Normal"


def _pq_status(pq: Optional[float]) -> str:
    if pq is None:   return "⚠ No PF data"
    if pq < 90:      return "🔴 CRITICAL — penalties being incurred"
    if pq < 95:      return "🟡 WARNING — below CoCT threshold"
    if pq < 97:      return "👀 WATCH — monitor at peak demand"
    return "✓ Good"


def _lsi_opportunity(billing: Dict, months: List[str]) -> Optional[float]:
    """Estimate monthly ZAR opportunity from shifting more loads to off-peak."""
    peak_offpeak_diff = 3.3396 - 1.7563   # R/kWh differential
    kwh_vals = [billing.get(m, {}).get("kwh", 0) or 0 for m in months]
    avg_kwh  = sum(kwh_vals) / len(kwh_vals) if kwh_vals else 0
    # Conservative: 10–15% of total kWh is shiftable to off-peak
    shiftable = avg_kwh * 0.12
    return round(shiftable * peak_offpeak_diff, 0) if avg_kwh > 0 else None


# ─── Period averaging helpers ────────────────────────────────────────────────

def _compute_period_averages(
    months: List[str],
    billing: Dict,
    cdd_data: Dict,
    pf_data: Dict,
) -> Dict:
    """Compute average KPI values for a list of months (for trend comparison)."""
    ei_list, ci_list, du_list, pq_list, lsi_list = [], [], [], [], []

    for m in months:
        b    = billing.get(m, {})
        cdd  = cdd_data.get(m, {}).get("cdd", 0) or 0
        kwh  = b.get("kwh", 0) or 0
        cost = b.get("cost", 0) or 0
        dem  = b.get("max_demand_kva", 0) or 0

        if cdd > 0 and kwh > 0: ei_list.append(kwh / cdd)
        if cdd > 0 and cost > 0: ci_list.append(cost / cdd)
        if _NMD_KVA > 0 and dem > 0: du_list.append(dem / _NMD_KVA * 100)

        pf_vals, pf_weights = [], []
        for pfc in _PFC_POINTS:
            pf_val = pf_data.get(pfc["label"], {}).get("monthly", {}).get(m)
            if pf_val and pf_val > 0.5:
                pf_vals.append(pf_val)
                pf_weights.append(pfc["weight"])
        if pf_vals:
            wp = sum(v * w for v, w in zip(pf_vals, pf_weights)) / sum(pf_weights)
            pq_list.append(wp * 100)

        op  = b.get("offpeak_kwh", 0) or 0
        tot = b.get("total_kwh_tou", 0) or kwh
        if tot > 0 and op > 0: lsi_list.append(op / tot * 100)

    def _avg(lst): return round(sum(lst) / len(lst), 1) if lst else None

    return {
        "energy_index":        _avg(ei_list),
        "cost_index":          _avg(ci_list),
        "demand_utilisation":  _avg(du_list),
        "power_quality_score": _avg(pq_list),
        "load_shift_index":    _avg(lsi_list),
    }


def _same_period_last_year(months: List[str]) -> List[str]:
    """Return the same calendar months from one year prior."""
    result = []
    for m in months:
        try:
            dt = datetime.strptime(m, "%Y-%m")
            ly = dt.replace(year=dt.year - 1)
            result.append(ly.strftime("%Y-%m"))
        except ValueError:
            pass
    return result


def _month_desc_to_key(desc: str) -> Optional[str]:
    """
    Convert Augos month description to YYYY-MM key.
    e.g. "Jan 26" → "2026-01", "Mar 25" → "2025-03"
    """
    if not desc or len(desc) < 6:
        return None
    try:
        abbr_map = {
            "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
            "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
            "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
        }
        parts = desc.strip().split()
        if len(parts) != 2:
            return None
        month_str, year_2 = parts
        month_num = abbr_map.get(month_str)
        if not month_num:
            return None
        year_full = f"20{year_2}" if int(year_2) < 50 else f"19{year_2}"
        return f"{year_full}-{month_num}"
    except Exception:
        return None
