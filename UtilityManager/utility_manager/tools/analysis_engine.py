"""
Analysis Engine — Exhaustive Analyst, Silent Reporter
======================================================
The agent's core intelligence loop.

Philosophy:
  - Ask EVERY relevant question internally, every time.
  - Score each finding for significance.
  - Suppress findings that are within normal bounds.
  - Return ONLY what is noteworthy, ranked by priority.

The length of the report is inversely proportional to the health of the system.
On a perfect day: "All clear. No action required."
"""

import logging
import math
from datetime import datetime
from typing import Any, Dict, List, Optional

from .augos_api import (
    get_electricity_consumption,
    get_water_consumption,
    get_gas_consumption,
    get_cost_analysis,
    get_power_factor,
    get_time_of_use,
)
from .weather_api import get_cape_town_weather
from .anomaly_detection import (
    detect_anomalies,
    analyze_base_load,
    check_power_factor_risk,
    check_demand_overage,
)
from .pattern_analysis import (
    analyze_consumption_patterns,
    year_on_year_comparison,
    calculate_carbon_footprint,
    identify_savings_opportunities,
    forecast_consumption,
)

log = logging.getLogger(__name__)

# ─── Significance Thresholds (tune as baselines are established) ─────────────

# A finding must score >= this to be surfaced (0–100 scale)
PERSONA_THRESHOLDS = {
    "chief_engineer":        15,   # Low — engineer wants early warning
    "general_manager":       45,   # High — GM only sees material issues
    "financial_controller":  30,   # Medium — financially material items
    "sustainability_officer": 25,  # Medium — trend changes matter
}

# Scoring weights — what makes a finding significant
def _score(
    deviation_pct: float = 0,
    z_score: float = 0,
    duration_days: int = 1,
    zar_impact: float = 0,
    earthcheck_band_change: bool = False,
    is_p1: bool = False,
) -> float:
    """
    Calculate a significance score for a finding (0–100).
    A finding is suppressed if its score is below the persona threshold.
    """
    score = 0.0
    score += min(30, abs(deviation_pct) * 0.8)       # Deviation (max 30pts)
    score += min(20, abs(z_score) * 5)                # Statistical rarity (max 20pts)
    score += min(15, duration_days * 3)               # Persistence (max 15pts)
    score += min(20, zar_impact / 500)                # Financial impact (max 20pts)
    score += 15 if earthcheck_band_change else 0      # Certification risk (15pts)
    score += 100 if is_p1 else 0                      # P1 always surfaces (override)
    return min(100, score)


# ─── Individual Checks ───────────────────────────────────────────────────────

def _check_electricity_base_load(point_id: int, base_load_result: Dict) -> Optional[Dict]:
    """Returns a finding if electricity base load is noteworthy, else None."""
    bl = base_load_result.get("base_load", {}).get("electricity", {})
    if bl.get("status") != "analysed":
        return None

    assessment = bl.get("assessment", "normal")
    trend_pct = bl.get("trend_percent", 0)
    flags = bl.get("flags", [])

    if not flags and assessment == "normal" and abs(trend_pct) < 10:
        return None  # All clear — suppress

    score = _score(deviation_pct=abs(trend_pct), duration_days=90)
    return {
        "category": "Electricity Base Load",
        "utility": "electricity",
        "severity": assessment,
        "score": score,
        "headline": flags[0] if flags else f"Base load trending {bl.get('trend_direction')} ({trend_pct:+.1f}%)",
        "detail": {
            "current_base_load_kw": bl.get("mean"),
            "trend_direction": bl.get("trend_direction"),
            "trend_percent": trend_pct,
            "window": bl.get("window"),
        },
        "action": "Audit always-on loads: standby HVAC zones, lighting, refrigeration efficiency.",
        "personas": ["chief_engineer"],
    }


def _check_water_base_load(point_id: int, base_load_result: Dict) -> Optional[Dict]:
    """Returns a finding if overnight water flow suggests a leak, else None."""
    bl = base_load_result.get("base_load", {}).get("water", {})
    if bl.get("status") != "analysed":
        return None

    mean_lph = bl.get("mean", 0)
    assessment = bl.get("assessment", "normal")
    flags = bl.get("flags", [])

    WARNING_LPH = 100
    CRITICAL_LPH = 200

    if mean_lph < WARNING_LPH and assessment == "normal":
        return None  # All clear — suppress

    is_p1 = mean_lph >= CRITICAL_LPH
    is_critical = assessment in ("P1_CRITICAL", "P2_WARNING")
    zar_est = mean_lph * 24 * 0.03  # Rough ZAR cost at ~R0.03/L

    score = _score(
        deviation_pct=((mean_lph - 50) / 50) * 100 if mean_lph > 50 else 0,
        duration_days=3,
        zar_impact=zar_est,
        is_p1=is_p1,
    )

    return {
        "category": "Water Leak Detection",
        "utility": "water",
        "severity": assessment,
        "score": score,
        "headline": flags[0] if flags else f"Overnight water flow elevated at {mean_lph:.0f} L/hr",
        "detail": {
            "overnight_flow_lph": round(mean_lph, 1),
            "threshold_warning_lph": WARNING_LPH,
            "threshold_critical_lph": CRITICAL_LPH,
            "estimated_daily_volume_kl": round(mean_lph * 24 / 1000, 2),
            "estimated_daily_cost_zar": round(zar_est, 2),
        },
        "action": "Immediate physical inspection of all water circuits. Check toilet cisterns, irrigation, pool auto-fill, and kitchen basement.",
        "personas": ["chief_engineer", "general_manager"] if is_p1 else ["chief_engineer"],
    }


def _check_gas_base_load(point_id: int, base_load_result: Dict) -> Optional[Dict]:
    """Returns a finding if gas is running outside kitchen hours, else None."""
    bl = base_load_result.get("base_load", {}).get("gas", {})
    if bl.get("status") != "analysed":
        return None

    assessment = bl.get("assessment", "normal")
    flags = bl.get("flags", [])

    if not flags and assessment == "normal":
        return None  # All clear — suppress

    return {
        "category": "Gas Base Load",
        "utility": "gas",
        "severity": assessment,
        "score": _score(deviation_pct=20, duration_days=7),
        "headline": flags[0] if flags else "Gas consumption elevated outside kitchen operating hours",
        "detail": {"mean_m3_per_hr": bl.get("mean"), "window": bl.get("window")},
        "action": "Check boiler cycling, kitchen equipment left on overnight, pilot lights.",
        "personas": ["chief_engineer"],
    }


def _check_power_factor(point_id: int) -> Optional[Dict]:
    """
    Check PF at SWITCH level (8324, 8336) — site-level PF (8323) is not diagnostic.
    Two independent PFC systems: Main Switch 1 (PFC-A) and Main Switch 2 (PFC-B).
    Returns a finding if either switch is below threshold.
    """
    PF_SWITCH_POINTS = [
        (8324, "Main Switch 1 (PFC-A)"),
        (8336, "Main Switch 2 (PFC-B)"),
    ]
    findings_for_caller = []

    for sw_id, sw_label in PF_SWITCH_POINTS:
        pf = check_power_factor_risk(sw_id)
        severity = pf.get("severity", "NO_DATA")
        avg_pf = pf.get("average_power_factor", 0)

        if severity in ("NO_DATA", "NORMAL", "P3_WATCH"):
            continue

        is_p1 = severity == "P1_CRITICAL"
        score = _score(
            deviation_pct=(0.95 - avg_pf) * 100,
            is_p1=is_p1,
            duration_days=30,
            zar_impact=40000 / 12,   # ~R40K annual saving potential / 12 months
        )

        findings_for_caller.append({
            "category": "Power Factor",
            "utility": "electricity",
            "severity": severity,
            "score": score,
            "headline": (
                f"{sw_label}: PF {avg_pf:.3f} — "
                f"{'CoCT penalties being incurred' if is_p1 else 'below 0.95 threshold — demand charge inflated'}"
            ),
            "detail": {
                "switch": sw_label,
                "average_pf": avg_pf,
                "minimum_pf": pf.get("minimum_power_factor"),
                "target_pf": 0.95,
                "max_demand_kva": pf.get("max_demand_kva"),
                "estimated_annual_saving": "R40,000–R77,000 (requires PFC Assessment to confirm)",
            },
            "action": (
                f"Contact Augos to arrange a PFC Assessment for {sw_label} "
                f"(<R5,000). The assessment will identify the root cause and provide accurate "
                f"pricing for the remedy. Main Switch 2 (PFC-B) can serve as reference — "
                f"it maintains PF 0.97+ consistently."
            ),
            "personas": ["chief_engineer", "general_manager"] if is_p1 else ["chief_engineer"],
        })

    # Return the worst finding (highest score), or None if all clear
    if not findings_for_caller:
        return None
    findings_for_caller.sort(key=lambda f: -f.get("score", 0))
    return findings_for_caller[0]


def _check_consumption_anomalies(point_id: int, anomaly_result: Dict) -> List[Dict]:
    """Returns findings for any statistically significant consumption anomalies."""
    findings = []
    for utility, data in anomaly_result.get("anomalies", {}).items():
        if not isinstance(data, dict) or data.get("status") != "analysed":
            continue

        p1_list = data.get("p1_critical", [])
        p2_list = data.get("p2_warning", [])

        for anomaly in p1_list + p2_list:
            is_p1 = anomaly in p1_list
            dev_pct = abs(anomaly.get("deviation_percent") or 0)
            z = abs(anomaly.get("z_score") or 0)
            score = _score(deviation_pct=dev_pct, z_score=z, is_p1=is_p1, duration_days=1)

            findings.append({
                "category": f"{utility.capitalize()} Consumption Anomaly",
                "utility": utility,
                "severity": "P1_CRITICAL" if is_p1 else "P2_WARNING",
                "score": score,
                "headline": f"{utility.capitalize()} {'spike' if anomaly.get('direction') == 'spike' else 'drop'}: {dev_pct:.0f}% {'above' if anomaly.get('direction') == 'spike' else 'below'} expected",
                "detail": {
                    "value": anomaly.get("value"),
                    "z_score": anomaly.get("z_score"),
                    "deviation_percent": dev_pct,
                    "expected_range": anomaly.get("expected_range"),
                    "unit": data.get("baseline_stats", {}).get("unit", ""),
                },
                "action": f"Investigate {utility} consumption spike — cross-reference with weather, occupancy, and operational changes.",
                "personas": ["chief_engineer", "general_manager"] if is_p1 else ["chief_engineer"],
            })

    return findings


def _check_yoy_trends(point_id: int) -> List[Dict]:
    """Returns findings only for utilities with significant YoY divergence."""
    yoy = year_on_year_comparison(point_id, utility="all")
    findings = []

    for utility, data in yoy.get("comparison", {}).items():
        pct = data.get("percent_change")
        if pct is None or abs(pct) < 10:
            continue  # Within 10% YoY — suppress

        is_increase = pct > 0
        score = _score(deviation_pct=abs(pct), duration_days=30, earthcheck_band_change=abs(pct) > 20)

        findings.append({
            "category": f"{utility.capitalize()} Year-on-Year Trend",
            "utility": utility,
            "severity": "P2_WARNING" if is_increase else "P3_POSITIVE",
            "score": score,
            "headline": f"{utility.capitalize()} {'UP' if is_increase else 'DOWN'} {abs(pct):.1f}% vs same period last year",
            "detail": {
                "current_total": data.get("current_period_total"),
                "prior_year_total": data.get("prior_year_period_total"),
                "absolute_delta": data.get("absolute_delta"),
                "percent_change": pct,
                "unit": data.get("unit", ""),
            },
            "action": (
                f"Investigate cause of {abs(pct):.1f}% {utility} increase vs prior year. Check occupancy changes, new equipment, operational changes."
                if is_increase else
                f"✅ {utility.capitalize()} reducing year-on-year — confirm EarthCheck data is captured for annual report."
            ),
            "personas": ["chief_engineer", "general_manager", "sustainability_officer"],
        })

    return findings


def _check_carbon_exposure(point_id: int) -> Optional[Dict]:
    """Returns a finding if carbon footprint is trending significantly vs prior period."""
    carbon = calculate_carbon_footprint(point_id, days=30)
    total_tco2e = carbon.get("totals", {}).get("total_tonnes_co2e", 0)
    carbon_tax_zar = carbon.get("carbon_tax", {}).get("estimated_exposure_zar", 0)

    # Only surface if carbon tax exposure is material (>R5,000/month)
    if carbon_tax_zar < 5000:
        return None

    score = _score(zar_impact=carbon_tax_zar, earthcheck_band_change=True, duration_days=30)

    return {
        "category": "Carbon Footprint",
        "utility": "electricity+gas",
        "severity": "P3_INSIGHT",
        "score": score,
        "headline": f"Monthly carbon exposure: {total_tco2e:.2f} tCO₂e — estimated carbon tax ZAR {carbon_tax_zar:,.0f}",
        "detail": carbon,
        "action": "Include in monthly EarthCheck report. Track trend vs prior period for sustainability KPI.",
        "personas": ["sustainability_officer", "financial_controller"],
    }


def _check_savings_opportunities(point_id: int) -> Optional[Dict]:
    """Surfaces savings opportunities only when they're likely material."""
    opps = identify_savings_opportunities(point_id)
    # For now, always include — but score keeps it filtered per persona
    score = 35  # Medium significance — surfaces for FC and CE, not GM
    return {
        "category": "Cost Optimisation Opportunities",
        "utility": "electricity",
        "severity": "P3_INSIGHT",
        "score": score,
        "headline": f"{opps.get('opportunities_found', 0)} actionable savings opportunities identified",
        "detail": {"opportunities": opps.get("opportunities", [])[:3]},
        "action": "Review top opportunities with Chief Engineer and Financial Controller.",
        "personas": ["financial_controller", "chief_engineer"],
    }


# ─── Master Analysis Runner ──────────────────────────────────────────────────

def run_full_analysis(point_id: int, persona: str = "chief_engineer") -> Dict[str, Any]:
    """
    Run the complete utility analysis checklist and return ONLY noteworthy findings.

    This is the exhaustive analyst: every relevant question is asked internally.
    Only findings that cross the significance threshold for the specified persona
    are returned. If everything is within normal bounds, returns an 'all clear'.

    The agent does not guess what's important — it checks everything and
    lets the significance scores decide what surfaces.

    Args:
        point_id: Augos Point ID (default 8323 — One & Only Cape Town)
        persona: 'chief_engineer' | 'general_manager' | 'financial_controller' | 'sustainability_officer'

    Returns:
        Dict with noteworthy findings only, ranked by priority. Includes 'all_clear'
        flag when nothing significant is found.
    """
    threshold = PERSONA_THRESHOLDS.get(persona, 30)
    all_findings: List[Dict] = []
    checks_run = []
    errors = []

    weather = get_cape_town_weather(days_back=7, days_forward=3)
    weather_summary = weather.get("historical", {}).get("summary", {})

    # 1. Base load analysis (electricity, water, gas)
    checks_run.append("base_load_all_utilities")
    try:
        base_load = analyze_base_load(point_id, utility="all", days=90)
        f = _check_electricity_base_load(point_id, base_load)
        if f:
            all_findings.append(f)
        f = _check_water_base_load(point_id, base_load)
        if f:
            all_findings.append(f)
        f = _check_gas_base_load(point_id, base_load)
        if f:
            all_findings.append(f)
    except Exception as e:
        errors.append(f"base_load: {e}")

    # 2. Anomaly detection (1-week window, all utilities)
    checks_run.append("anomaly_detection_7d")
    try:
        anomalies = detect_anomalies(point_id, utility="all", days=7)
        all_findings.extend(_check_consumption_anomalies(point_id, anomalies))
    except Exception as e:
        errors.append(f"anomaly_detection: {e}")

    # 3. Power factor risk
    checks_run.append("power_factor_risk")
    try:
        f = _check_power_factor(point_id)
        if f:
            all_findings.append(f)
    except Exception as e:
        errors.append(f"power_factor: {e}")

    # 4. Year-on-year trends (all utilities)
    checks_run.append("year_on_year_all")
    try:
        all_findings.extend(_check_yoy_trends(point_id))
    except Exception as e:
        errors.append(f"yoy_trends: {e}")

    # 5. Carbon exposure (monthly)
    checks_run.append("carbon_footprint_30d")
    try:
        f = _check_carbon_exposure(point_id)
        if f:
            all_findings.append(f)
    except Exception as e:
        errors.append(f"carbon: {e}")

    # 6. Savings opportunities (throttled — monthly cadence)
    checks_run.append("savings_opportunities")
    try:
        f = _check_savings_opportunities(point_id)
        if f:
            all_findings.append(f)
    except Exception as e:
        errors.append(f"savings: {e}")

    # Deduplicate — same anomaly can appear once per sub-meter; keep unique by headline
    seen_headlines: set = set()
    unique_findings: list = []
    for f in all_findings:
        key = f.get("headline", "")
        if key not in seen_headlines:
            seen_headlines.add(key)
            unique_findings.append(f)
    all_findings = unique_findings

    # Filter by persona and significance threshold

    persona_findings = [
        f for f in all_findings
        if persona in f.get("personas", []) and f.get("score", 0) >= threshold
    ]

    # Sort: P1 Critical first, then by score descending
    def _sort_key(f):
        sev_order = {"P1_CRITICAL": 0, "P2_WARNING": 1, "P3_INSIGHT": 2, "P3_POSITIVE": 3, "normal": 4}
        return (sev_order.get(f.get("severity", "normal"), 4), -f.get("score", 0))

    persona_findings.sort(key=_sort_key)

    p1_count = sum(1 for f in persona_findings if f.get("severity") == "P1_CRITICAL")
    p2_count = sum(1 for f in persona_findings if f.get("severity") == "P2_WARNING")
    p3_count = sum(1 for f in persona_findings if f.get("severity") in ("P3_INSIGHT", "P3_POSITIVE"))

    all_clear = len(persona_findings) == 0

    return {
        "point_id": point_id,
        "persona": persona,
        "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
        "checks_run": len(checks_run),
        "checks_list": checks_run,
        "weather_context": {
            "temp_min_c": weather_summary.get("temperature", {}).get("min_c"),
            "temp_max_c": weather_summary.get("temperature", {}).get("max_c"),
            "precipitation_mm": weather_summary.get("precipitation_total_mm"),
        },
        "all_clear": all_clear,
        "all_clear_message": (
            "✅ All utilities within normal parameters. No action required."
            if all_clear else None
        ),
        "findings_summary": {
            "total": len(persona_findings),
            "p1_critical": p1_count,
            "p2_warning": p2_count,
            "p3_insight": p3_count,
        },
        "findings": persona_findings,
        "suppressed_count": len(all_findings) - len(persona_findings),
        "errors": errors if errors else None,
    }


def run_engineering_brief(point_id: int = 8323) -> Dict[str, Any]:
    """
    Run the Chief Engineer's full analysis and return only actionable findings.

    Asks every engineering-relevant question internally. Returns 'All clear' if
    everything is within normal parameters. Only anomalies, threshold breaches,
    and noteworthy trends are surfaced — normal metrics are suppressed.

    Args:
        point_id: Augos Point ID (default: 8323)

    Returns:
        Engineering brief with only noteworthy findings for the Chief Engineer.
    """
    return run_full_analysis(point_id, persona="chief_engineer")


def run_executive_brief(point_id: int = 8323) -> Dict[str, Any]:
    """
    Run the GM's analysis and return only findings material enough for executive attention.

    Applies a high significance threshold — the GM only sees genuinely material
    issues, not routine engineering checks. Normal operations produce a one-line
    'All clear' response.

    Args:
        point_id: Augos Point ID (default: 8323)

    Returns:
        Executive brief with high-significance findings only.
    """
    return run_full_analysis(point_id, persona="general_manager")


def run_sustainability_brief(point_id: int = 8323) -> Dict[str, Any]:
    """
    Run the Sustainability Officer's analysis focused on EarthCheck KPIs and trends.

    Checks carbon exposure, YoY consumption trends, base load efficiency,
    and EarthCheck benchmark band positioning. Only surfaces noteworthy changes.

    Args:
        point_id: Augos Point ID (default: 8323)

    Returns:
        Sustainability findings that warrant the Sustainability Officer's attention.
    """
    return run_full_analysis(point_id, persona="sustainability_officer")


def run_financial_brief(point_id: int = 8323) -> Dict[str, Any]:
    """
    Run the Financial Controller's analysis focused on cost and billing.

    Checks tariff efficiency, YoY cost trends, carbon tax exposure, and
    savings opportunities. Only surfaces financially material findings.

    Args:
        point_id: Augos Point ID (default: 8323)

    Returns:
        Financial findings that warrant the Financial Controller's attention.
    """
    return run_full_analysis(point_id, persona="financial_controller")
