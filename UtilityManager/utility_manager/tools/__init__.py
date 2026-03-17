"""
tools/__init__.py — Utility Manager Tool Registry

Primary entry points (Exhaustive Analyst, Silent Reporter):
  run_engineering_brief()     — Chief Engineer (checks everything, reports only anomalies)
  run_executive_brief()       — General Manager (high threshold, executive language)
  run_sustainability_brief()  — Sustainability Officer (EarthCheck KPIs, trends)
  run_financial_brief()       — Financial Controller (cost, billing, savings)

Underlying tools are also individually accessible for targeted on-demand queries.
"""

from .augos_api import (
    resolve_site,
    get_site_overview,
    get_electricity_consumption,
    get_water_consumption,
    get_gas_consumption,
    get_all_utility_consumption,
    get_cost_analysis,
    get_bill_verification,
    get_cost_allocation,
    get_tariff_comparison,
    get_power_factor,
    get_time_of_use,
    get_technical_analysis,
    get_dashboard,
    get_live_curtailment_status,
    get_sensor_readings,
)

from .weather_api import (
    get_cape_town_weather,
    correlate_utility_with_weather,
)

from .anomaly_detection import (
    detect_anomalies,
    analyze_base_load,
    check_power_factor_risk,
    check_demand_overage,
)

from .pattern_analysis import (
    analyze_consumption_patterns,
    forecast_consumption,
    year_on_year_comparison,
    identify_savings_opportunities,
    calculate_carbon_footprint,
)

from .analysis_engine import (
    run_engineering_brief,
    run_executive_brief,
    run_sustainability_brief,
    run_financial_brief,
    run_full_analysis,
)

from .email_sender import (
    send_engineering_brief,
    send_executive_brief,
    send_sustainability_report,
    send_financial_report,
    send_immediate_alert,
    test_email_connection,
)

__all__ = [
    # ── Primary Analysis Entry Points (Exhaustive Analyst, Silent Reporter) ──
    "run_engineering_brief",
    "run_executive_brief",
    "run_sustainability_brief",
    "run_financial_brief",
    "run_full_analysis",
    # ── Augos API (targeted queries) ──
    "resolve_site",
    "get_site_overview",
    "get_electricity_consumption",
    "get_water_consumption",
    "get_gas_consumption",
    "get_all_utility_consumption",
    "get_cost_analysis",
    "get_bill_verification",
    "get_cost_allocation",
    "get_tariff_comparison",
    "get_power_factor",
    "get_time_of_use",
    "get_technical_analysis",
    "get_dashboard",
    "get_live_curtailment_status",
    "get_sensor_readings",
    # Weather
    "get_cape_town_weather",
    "correlate_utility_with_weather",
    # Anomaly Detection
    "detect_anomalies",
    "analyze_base_load",
    "check_power_factor_risk",
    "check_demand_overage",
    # Pattern Analysis & Reporting
    "analyze_consumption_patterns",
    "forecast_consumption",
    "year_on_year_comparison",
    "identify_savings_opportunities",
    "calculate_carbon_footprint",
]
