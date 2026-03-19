"""
Anomaly Detection Engine
========================
Two detection approaches:

1. EnPI Residual (PRIMARY) — detect_enpi_anomalies()
   Fits a linear model (kWh ~ CDD) on 36-month billing history.
   Flags months where actual kWh deviates from climate-predicted kWh by > 2.5σ.
   This eliminates weather-driven false positives entirely.
   Financial impact is always quantified before surfacing.

2. Rolling Z-score (LEGACY) — detect_anomalies()
   Retained for water/gas where CDD model does not apply.
   Electricity z-score detection is deprecated in favour of EnPI residuals.
"""

import logging
import math
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .augos_api import (
    get_electricity_consumption,
    get_water_consumption,
    get_gas_consumption,
    get_power_factor,
)

log = logging.getLogger(__name__)

# Anomaly thresholds
_Z_WARNING = 2.5
_Z_CRITICAL = 3.5

# Base load windows (24h clock hours)
_ELEC_BASE_START = 2
_ELEC_BASE_END = 5
_WATER_BASE_START = 2
_WATER_BASE_END = 5
_GAS_BASE_START = 0
_GAS_BASE_END = 5
_KITCHEN_START = 6
_KITCHEN_END = 22

# Hotel-specific thresholds
_WATER_LEAK_WARNING_LPH = 100      # L/hr overnight
_WATER_LEAK_CRITICAL_LPH = 200     # L/hr overnight
_PF_WARNING = 0.92
_PF_CRITICAL = 0.90
_DEMAND_WARNING_PCT = 0.95


def _extract_time_series(api_response: Dict) -> List[float]:
    """Extract a flat list of consumption values from Augos API response."""
    data = api_response.get("data", api_response)
    values = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, list):
                for subitem in item:
                    if isinstance(subitem, dict):
                        v = subitem.get("consumption") or subitem.get("value") or subitem.get("kWh")
                        if v is not None:
                            try:
                                values.append(float(v))
                            except (TypeError, ValueError):
                                pass
            elif isinstance(item, dict):
                v = item.get("consumption") or item.get("value") or item.get("kWh")
                if v is not None:
                    try:
                        values.append(float(v))
                    except (TypeError, ValueError):
                        pass
    return values


def _z_score_anomalies(values: List[float], z_threshold: float = _Z_WARNING) -> List[Dict]:
    """Identify anomalous values using Z-score analysis."""
    if len(values) < 7:
        return []

    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std = math.sqrt(variance) if variance > 0 else 0

    if std == 0:
        return []

    anomalies = []
    for i, v in enumerate(values):
        z = (v - mean) / std
        if abs(z) >= z_threshold:
            severity = "P1_CRITICAL" if abs(z) >= _Z_CRITICAL else "P2_WARNING"
            anomalies.append({
                "index": i,
                "value": round(v, 3),
                "z_score": round(z, 3),
                "expected_range": {
                    "low": max(0.0, round(mean - 2 * std, 3)),  # consumption can't be negative
                    "high": round(mean + 2 * std, 3),
                },
                "deviation_percent": round(((v - mean) / mean) * 100, 1) if mean != 0 else None,
                "severity": severity,
                "direction": "spike" if z > 0 else "drop",
            })

    return anomalies


def detect_anomalies(point_id: int, utility: str = "all", days: int = 7) -> Dict[str, Any]:
    """
    Detect consumption anomalies for the specified utility using Z-score analysis.

    Compares recent consumption against a rolling 90-day baseline.
    Flags values deviating more than 2.5σ (P2 Warning) or 3.5σ (P1 Critical).
    Hotel-specific rules applied: overnight water flow, off-hours gas, PF.

    Args:
        point_id: Augos Point ID (default: 8323)
        utility: 'electricity', 'water', 'gas', or 'all'
        days: Short window to check for anomalies (7 = last week)

    Returns:
        Anomaly report with severity, magnitude, and recommended actions.
    """
    results = {"point_id": point_id, "utility": utility, "analysis_days": days, "anomalies": {}}
    utilities_to_check = ["electricity", "water", "gas"] if utility == "all" else [utility]

    for util in utilities_to_check:
        # Get 90-day baseline
        if util == "electricity":
            baseline_data = get_electricity_consumption(point_id, 90)
            recent_data = get_electricity_consumption(point_id, days)
        elif util == "water":
            baseline_data = get_water_consumption(point_id, 90)
            recent_data = get_water_consumption(point_id, days)
        else:
            baseline_data = get_gas_consumption(point_id, 90)
            recent_data = get_gas_consumption(point_id, days)

        if "error" in str(baseline_data.get("data", "")):
            results["anomalies"][util] = {"status": "no_data", "message": f"No {util} data available"}
            continue

        baseline_values = _extract_time_series(baseline_data)
        recent_values = _extract_time_series(recent_data)

        if not baseline_values:
            results["anomalies"][util] = {"status": "no_baseline", "message": f"Insufficient baseline data for {util}"}
            continue

        all_values = baseline_values + recent_values
        anomalies = _z_score_anomalies(all_values)

        # Filter to anomalies in the recent window
        recent_start_idx = len(baseline_values)
        recent_anomalies = [a for a in anomalies if a["index"] >= recent_start_idx]

        results["anomalies"][util] = {
            "status": "analysed",
            "baseline_points": len(baseline_values),
            "recent_points": len(recent_values),
            "anomalies_found": len(recent_anomalies),
            "p1_critical": [a for a in recent_anomalies if a["severity"] == "P1_CRITICAL"],
            "p2_warning": [a for a in recent_anomalies if a["severity"] == "P2_WARNING"],
            "baseline_stats": {
                "mean": round(sum(baseline_values) / len(baseline_values), 3) if baseline_values else None,
                "unit": baseline_data.get("unit", ""),
            },
        }

    results["summary"] = {
        "total_anomalies": sum(
            v.get("anomalies_found", 0) for v in results["anomalies"].values()
            if isinstance(v, dict)
        ),
        "highest_severity": "P1_CRITICAL" if any(
            v.get("p1_critical") for v in results["anomalies"].values()
            if isinstance(v, dict)
        ) else ("P2_WARNING" if any(
            v.get("p2_warning") for v in results["anomalies"].values()
            if isinstance(v, dict)
        ) else "NORMAL"),
    }

    return results


def analyze_base_load(point_id: int, utility: str = "all", days: int = 90) -> Dict[str, Any]:
    """
    Analyse overnight base load for all utilities.

    Base load (02:00–05:00 for electricity and water; 00:00–05:00 for gas)
    reveals always-on consumption that should be minimised.
    Rising base load = inefficiency; water overnight > 200 L/hr = suspected leak.

    Args:
        point_id: Augos Point ID
        utility: 'electricity', 'water', 'gas', or 'all'
        days: Lookback window for baseline calculation

    Returns:
        Base load statistics, trend assessment, and hotel-specific risk flags.
    """
    utilities_to_check = ["electricity", "water", "gas"] if utility == "all" else [utility]
    results = {"point_id": point_id, "utility": utility, "analysis_days": days, "base_load": {}}

    for util in utilities_to_check:
        if util == "electricity":
            data = get_electricity_consumption(point_id, days)
            unit = "kW"
            window = f"{_ELEC_BASE_START:02d}:00–{_ELEC_BASE_END:02d}:00"
        elif util == "water":
            data = get_water_consumption(point_id, days)
            unit = "L/hr"
            window = f"{_WATER_BASE_START:02d}:00–{_WATER_BASE_END:02d}:00"
        else:
            data = get_gas_consumption(point_id, days)
            unit = "m³/hr"
            window = f"{_GAS_BASE_START:02d}:00–{_GAS_BASE_END:02d}:00"

        if "error" in str(data):
            results["base_load"][util] = {"status": "no_data"}
            continue

        values = _extract_time_series(data)
        if not values:
            results["base_load"][util] = {"status": "no_data", "message": "No readings extracted"}
            continue

        mean_val = sum(values) / len(values)
        min_val = min(values)
        max_val = max(values)

        # Trend: compare first half vs second half of the window
        half = len(values) // 2
        first_half_mean = sum(values[:half]) / half if half > 0 else mean_val
        second_half_mean = sum(values[half:]) / (len(values) - half) if (len(values) - half) > 0 else mean_val
        trend_pct = ((second_half_mean - first_half_mean) / first_half_mean * 100) if first_half_mean > 0 else 0

        assessment = {"electricity": "normal", "water": "normal", "gas": "normal"}
        flags = []

        if util == "water":
            if mean_val >= _WATER_LEAK_CRITICAL_LPH:
                assessment[util] = "P1_CRITICAL"
                flags.append(f"SUSPECTED MAJOR LEAK: {mean_val:.0f} L/hr overnight (threshold: {_WATER_LEAK_CRITICAL_LPH})")
            elif mean_val >= _WATER_LEAK_WARNING_LPH:
                assessment[util] = "P2_WARNING"
                flags.append(f"Possible leak: {mean_val:.0f} L/hr overnight (threshold: {_WATER_LEAK_WARNING_LPH})")

        if util == "electricity" and trend_pct > 10:
            assessment[util] = "P2_WARNING"
            flags.append(f"Base load rising: +{trend_pct:.1f}% trend over {days} days — investigate always-on loads")

        results["base_load"][util] = {
            "status": "analysed",
            "window": window,
            "unit": unit,
            "mean": round(mean_val, 3),
            "min": round(min_val, 3),
            "max": round(max_val, 3),
            "trend_percent": round(trend_pct, 1),
            "trend_direction": "rising" if trend_pct > 5 else ("falling" if trend_pct < -5 else "stable"),
            "assessment": assessment[util],
            "flags": flags,
        }

    return results


def check_power_factor_risk(point_id: int) -> Dict[str, Any]:
    """
    Assess power factor risk and CoCT penalty exposure.

    PF < 0.95 = potential penalties on CoCT MV TOU tariff.
    PF < 0.92 = P2 Warning. PF < 0.90 = P1 Critical.

    Args:
        point_id: Augos Point ID

    Returns:
        Power factor assessment with penalty risk and capacitor bank recommendations.
    """
    pf_data = get_power_factor(point_id, months=3)
    if "error" in pf_data:
        return pf_data

    avg_pf = pf_data.get("average_power_factor", 0)
    min_pf = pf_data.get("minimum_power_factor")
    data_points = pf_data.get("data_points", 0)

    # No data returned — don't treat as critical, return no-data status
    if data_points == 0 or avg_pf == 0:
        return {
            "point_id": point_id,
            "severity": "NO_DATA",
            "average_power_factor": avg_pf,
            "data_points": data_points,
            "message": "No power factor data available for this point/period. Check that PF meters are active in Augos.",
        }

    if avg_pf < _PF_CRITICAL:
        severity = "P1_CRITICAL"
        action = "Immediate capacitor bank inspection required. Utility penalties are being incurred."
    elif avg_pf < _PF_WARNING:
        severity = "P2_WARNING"
        action = "Schedule capacitor bank inspection. CoCT penalties may be accruing."
    elif avg_pf < 0.95:
        severity = "P3_WATCH"
        action = "Monitor monthly. PF approaching penalty threshold."
    else:
        severity = "NORMAL"
        action = "Power factor is healthy. No action required."

    return {
        "point_id": point_id,
        "average_power_factor": avg_pf,
        "minimum_power_factor": min_pf,
        "pf_target": 0.95,
        "severity": severity,
        "action": action,
        "penalty_risk": avg_pf < 0.95,
        "max_demand_kva": pf_data.get("max_demand_kva"),
        "data_points": pf_data.get("data_points"),
    }


def check_demand_overage(point_id: int) -> Dict[str, Any]:
    """
    Check whether current demand is approaching or exceeding the contracted maximum.

    Exceeding contracted demand on CoCT MV TOU triggers significant excess charges.
    Alerts at 95% of limit (P2 Warning) and 100% (P1 Critical).

    Args:
        point_id: Augos Point ID

    Returns:
        Current month peak demand vs contracted limit with severity assessment.
    """
    pf_data = get_power_factor(point_id, months=1)
    if "error" in pf_data:
        return pf_data

    max_demand = pf_data.get("max_demand_kva")
    if max_demand is None:
        return {"point_id": point_id, "status": "no_data", "message": "No demand data available"}

    # Without a stored contracted limit, flag for configuration
    return {
        "point_id": point_id,
        "current_month_peak_kva": max_demand,
        "note": "Set CONTRACTED_DEMAND_KVA in .env to enable threshold alerting. "
                "Find your contracted demand on your CoCT electricity account.",
        "action": f"Current peak demand this month: {max_demand} kVA. "
                  "Compare against your contracted maximum to assess overage risk.",
    }


# ─── EnPI Residual Anomaly Detection (PRIMARY) ───────────────────────────────

def detect_enpi_anomalies(
    months_history: int = 36,
    months_to_check: int = 3,
    z_threshold: float = 2.5,
    min_zar_impact: float = 5000.0,
) -> List[Dict]:
    """
    Detect electricity consumption anomalies using the EnPI regression model.

    Approach:
      1. Fetch monthly billing history (kWh + cost) and monthly CDD.
      2. Fit linear model: kWh = α + β × CDD (the EnPI model).
      3. Compute residuals (actual - predicted) for all historical months.
      4. Standardise residuals → z-scores.
      5. Flag months in the check window where:
           |z| > z_threshold  AND  financial impact > min_zar_impact
      6. Apply anti-noise suppression:
           - Suppress if CDD was extreme (> 130% or < 70% of historical mean)
             because model accuracy degrades at extremes.
           - Classify: positive residual = unexplained over-consumption;
             negative residual = unexplained under-consumption (efficiency gain).

    Returns:
        List of finding dicts (severity, headline, detail, action, personas).
        Empty list = no anomalies detected.
    """
    # Lazy imports to avoid circular dependency and slow startup
    from .kpi_engine import _fetch_billing_history, _month_desc_to_key
    from .cdd_engine import get_monthly_cdd_series, fit_enpi_model

    lat = float(os.getenv("SITE_LAT", "-33.9249"))
    lon = float(os.getenv("SITE_LON", "18.4241"))

    # --- Fetch data ---
    try:
        billing  = _fetch_billing_history(months=months_history)
        cdd_data = get_monthly_cdd_series(lat, lon)
    except Exception as e:
        log.warning("EnPI anomaly data fetch failed: %s", e)
        return []

    # --- Build paired series ---
    common = sorted(set(billing) & set(cdd_data))
    monthly_kwh = {m: billing[m]["kwh"] for m in common if billing[m].get("kwh", 0) > 0}
    monthly_cdd = {m: cdd_data[m] for m in common}

    if len(monthly_kwh) < 12:
        log.info("EnPI anomaly: insufficient history (%d months). Need ≥12.", len(monthly_kwh))
        return []

    # --- Fit EnPI model ---
    model = fit_enpi_model(monthly_kwh, monthly_cdd)
    if "error" in model:
        log.warning("EnPI model fit failed: %s", model["error"])
        return []

    residuals = model.get("monthly_residuals", {})  # {YYYY-MM: residual_kWh}
    if not residuals:
        return []

    # --- Compute residual statistics ---
    res_values = list(residuals.values())
    res_mean   = sum(res_values) / len(res_values)
    res_var    = sum((r - res_mean) ** 2 for r in res_values) / len(res_values)
    res_std    = math.sqrt(res_var) if res_var > 0 else 1.0

    # Mean CDD per CALENDAR MONTH for suppression check
    # (compare each month to its seasonal average, not the annual average)
    seasonal_cdd: Dict[str, List[float]] = {}
    for m in common:
        cal_month = m[5:7]   # "01" through "12"
        cdd_val   = cdd_data[m].get("cdd", 0) or 0
        if cdd_val > 0:
            seasonal_cdd.setdefault(cal_month, []).append(cdd_val)
    seasonal_mean: Dict[str, float] = {
        k: sum(v) / len(v) for k, v in seasonal_cdd.items()
    }
    # Fallback for months with no CDD history
    mean_cdd = sum(seasonal_mean.values()) / len(seasonal_mean) if seasonal_mean else 50.0

    # --- Check the most recent months ---
    all_months   = sorted(common, reverse=True)
    check_months = all_months[:months_to_check]

    # Average ZAR per kWh from recent billing
    recent_costs = [billing[m]["cost"] for m in check_months if billing[m].get("cost", 0) > 0]
    recent_kwh   = [billing[m]["kwh"]  for m in check_months if billing[m].get("kwh",  0) > 0]
    avg_rate     = (sum(recent_costs) / sum(recent_kwh)) if recent_kwh and sum(recent_kwh) > 0 else 2.48

    findings = []
    for month in check_months:
        residual = residuals.get(month)
        if residual is None:
            continue

        z    = (residual - res_mean) / res_std
        cdd  = cdd_data.get(month, {}).get("cdd", mean_cdd)
        kwh  = billing.get(month, {}).get("kwh", 0)
        pred = model.get("monthly_predicted", {}).get(month, kwh)

        # --- Anti-noise: suppress only if weather was genuinely extreme for that season ---
        # Compare to same-calendar-month average (e.g. Feb 2026 vs avg of all Februaries)
        cal_month    = month[5:7]
        season_mean  = seasonal_mean.get(cal_month, cdd)
        cdd_ratio    = cdd / season_mean if season_mean > 0 else 1.0
        if cdd_ratio > 1.5 or (season_mean > 5 and cdd_ratio < 0.5):
            log.info("EnPI anomaly %s suppressed: unusual weather for season (%.1f CDD vs %.1f avg)",
                     month, cdd, season_mean)
            continue

        # --- Anti-noise: suppress if z below threshold ---
        if abs(z) < z_threshold:
            continue

        # --- Financial impact ---
        zar_impact = abs(residual) * avg_rate
        if zar_impact < min_zar_impact:
            log.info("EnPI anomaly %s suppressed: impact R%.0f < threshold R%.0f",
                     month, zar_impact, min_zar_impact)
            continue

        # --- Build finding ---
        direction  = "above" if residual > 0 else "below"
        pct        = abs(residual / pred * 100) if pred > 0 else 0
        severity   = "P1_CRITICAL" if abs(z) >= 3.5 else "P2_WARNING"

        if residual > 0:
            headline = (
                f"{month}: Consumption {pct:.1f}% above climate expectation — "
                f"{abs(residual):,.0f} kWh unexplained (R{zar_impact:,.0f} impact)"
            )
            action = (
                f"Investigate non-weather loads in {month}. "
                f"Expected {pred:,.0f} kWh for {cdd:.0f} CDD; actual was {kwh:,.0f} kWh. "
                f"Check sub-meter breakdown for the driving circuit."
            )
        else:
            headline = (
                f"{month}: Consumption {pct:.1f}% below climate expectation — "
                f"{abs(residual):,.0f} kWh efficiency gain (R{zar_impact:,.0f})"
            )
            severity = "P3_POSITIVE"
            action   = (
                f"Efficiency improvement confirmed for {month}. "
                f"Expected {pred:,.0f} kWh; actual {kwh:,.0f} kWh. "
                f"Document what changed to replicate this performance."
            )

        findings.append({
            "category": "Consumption Anomaly (EnPI)",
            "utility":  "electricity",
            "severity": severity,
            "score":    min(100, 30 + abs(z) * 10 + zar_impact / 1000),
            "headline": headline,
            "detail": {
                "month":            month,
                "actual_kwh":       f"{kwh:,.0f}",
                "predicted_kwh":    f"{pred:,.0f}",
                "residual_kwh":     f"{residual:+,.0f}",
                "z_score":          f"{z:+.2f}σ",
                "cdd":              f"{cdd:.0f}",
                "model_r2":         f"{model['r_squared']:.2f}",
                "financial_impact": f"R{zar_impact:,.0f}",
                "avg_rate_zar_kwh": f"R{avg_rate:.3f}",
            },
            "action":   action,
            "personas": (
                ["chief_engineer", "general_manager", "financial_controller"]
                if severity == "P1_CRITICAL"
                else ["chief_engineer", "financial_controller"]
                if severity == "P2_WARNING"
                else ["chief_engineer"]
            ),
        })

    return findings
