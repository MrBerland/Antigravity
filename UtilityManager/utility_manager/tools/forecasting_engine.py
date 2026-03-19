"""
Forecasting Engine — Month-End Accrual + Annual Budget
=======================================================
Forecast methodology (revised):

EnPI model insight:
  This hotel's electricity is OCCUPANCY-driven, not weather-driven.
  R² ≈ 0 confirms CDD explains <5% of monthly consumption variance.
  The CDD model is retained for RELATIVE performance assessment (Energy Index)
  but is NOT used for absolute consumption forecasting.

Forecast baseline (CORRECT for this property):
  Seasonal calendar-month average: mean kWh for each calendar month
  computed from the 3 most recent full years (2023, 2024, 2025), which
  excludes the 2021-2022 COVID/renovation period distortion.

Outputs:
  1. month_end_forecast()   — This month's projected kWh and ZAR cost
  2. annual_budget_forecast() — Full year projection, actuals + seasonal forecast
  3. tou_shift_analysis()   — TOU load-shift financial opportunity

All ZAR cost estimates include:
  - Consumption (blended TOU rate)
  - Demand charge (kVA × R155.50, from calendar-month historical peak average)
  - Network access charge (~R4,200/month)
  - July tariff increase of 12% applied from month 7 onward
"""

import logging
import os
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

log = logging.getLogger(__name__)

# ─── Constants ────────────────────────────────────────────────────────────────

_RATE_PEAK      = 3.3396   # ZAR/kWh — CoCT MV TOU peak
_RATE_STANDARD  = 2.1708   # ZAR/kWh — standard
_RATE_OFFPEAK   = 1.7563   # ZAR/kWh — off-peak
_RATE_DEMAND    = 155.50   # ZAR/kVA — Nightsave Urban High Demand charge
_RATE_NAC       = 140.0    # ZAR/day — network access (~R4,200/month)
_TARIFF_INCREASE_PCT = 12.0  # % — July tariff increase estimate

_TOU_OFFPEAK_PCT  = 0.53
_TOU_STANDARD_PCT = 0.30
_TOU_PEAK_PCT     = 0.17

_LAT = float(os.getenv("SITE_LAT", "-33.9249"))
_LON = float(os.getenv("SITE_LON", "18.4241"))

# Use only these years for the seasonal baseline (post-COVID, post-renovation)
_BASELINE_YEARS = [2023, 2024, 2025]


# ─── Rate helpers ─────────────────────────────────────────────────────────────

def _blended_rate() -> float:
    return (_TOU_OFFPEAK_PCT  * _RATE_OFFPEAK
            + _TOU_STANDARD_PCT * _RATE_STANDARD
            + _TOU_PEAK_PCT    * _RATE_PEAK)


def _kwh_to_zar(kwh: float, rate: float = None) -> float:
    return kwh * (rate or _blended_rate())


def _apply_tariff_increase(rate: float, month: int) -> float:
    """Apply July tariff increase to post-June months."""
    return rate * (1 + _TARIFF_INCREASE_PCT / 100) if month >= 7 else rate


# ─── Seasonal kWh baseline ────────────────────────────────────────────────────

def _seasonal_kwh_baseline(billing: Dict) -> Dict[str, Dict]:
    """
    Compute seasonal kWh statistics per calendar month (01–12).

    Uses only _BASELINE_YEARS (2023–2025) to exclude COVID/renovation distortion.
    For each calendar month, returns: avg, std, p10, p90, count, samples.

    Args:
        billing: Monthly billing dict from _fetch_billing_history()

    Returns:
        {"01": {"avg": float, "std": float, "p10": float, "p90": float, ...}, ...}
    """
    buckets: Dict[str, List[float]] = {}
    demand_buckets: Dict[str, List[float]] = {}

    for ym, data in billing.items():
        try:
            yr  = int(ym[:4])
            cal = ym[5:7]
        except (ValueError, IndexError):
            continue

        if yr not in _BASELINE_YEARS:
            continue

        kwh = data.get("kwh", 0) or 0
        dem = data.get("max_demand_kva", 0) or 0

        if kwh > 0:
            # Exclude obvious outliers (< 400K kWh = likely partial month or shutdown)
            if kwh > 400_000:
                buckets.setdefault(cal, []).append(kwh)
        if dem > 0:
            demand_buckets.setdefault(cal, []).append(dem)

    result = {}
    for cal, values in buckets.items():
        n       = len(values)
        avg     = sum(values) / n
        var     = sum((v - avg) ** 2 for v in values) / n
        std     = var ** 0.5

        # Sort for percentiles
        sorted_v = sorted(values)
        p10_idx  = max(0, int(0.10 * n) - 1)
        p90_idx  = min(n - 1, int(0.90 * n))

        dem_vals   = demand_buckets.get(cal, [])
        avg_demand = sum(dem_vals) / len(dem_vals) if dem_vals else 1200.0

        result[cal] = {
            "avg":        round(avg, 0),
            "std":        round(std, 0),
            "p10":        round(sorted_v[p10_idx], 0),
            "p90":        round(sorted_v[p90_idx], 0),
            "count":      n,
            "samples":    [round(v, 0) for v in sorted_v],
            "avg_demand_kva": round(avg_demand, 0),
        }

    return result


# ─── 1. Month-End Accrual Forecast ───────────────────────────────────────────

def month_end_forecast() -> Dict[str, Any]:
    """
    Forecast this month's final kWh consumption and ZAR cost.

    Method:
      - Uses the seasonal baseline for this calendar month (3-year avg).
      - Adjusts for elapsed fraction of month using CDD ratio:
        If current month CDD-to-date is higher than seasonal average for
        this point in month, we nudge the forecast up accordingly.
      - P10/P90 taken directly from historical spread of this calendar month.

    Returns:
        Forecast dict with kwh and cost estimates, vs same month last year.
    """
    from .cdd_engine import get_current_month_cdd
    from .kpi_engine import _fetch_billing_history

    today  = date.today()
    ym     = today.strftime("%Y-%m")
    yr, mo = today.year, today.month
    cal    = f"{mo:02d}"
    ly_ym  = f"{yr - 1}-{cal}"

    billing     = _fetch_billing_history(months=48)
    baseline    = _seasonal_kwh_baseline(billing)
    current_cdd = get_current_month_cdd(_LAT, _LON)

    if cal not in baseline:
        return {"error": f"No seasonal baseline for calendar month {cal}. "
                f"Need data from {_BASELINE_YEARS}."}

    bas = baseline[cal]
    avg_kwh    = bas["avg"]
    std_kwh    = bas["std"]
    p10_kwh    = bas["p10"]
    p90_kwh    = bas["p90"]
    avg_demand = bas["avg_demand_kva"]

    # CDD context (informational, mild adjustment)
    cdd_actual   = current_cdd.get("cdd_actual", 0)
    cdd_forecast = current_cdd.get("cdd_forecast", 0)
    cdd_total    = current_cdd.get("cdd_total_estimate", cdd_actual + cdd_forecast)
    days_done    = current_cdd.get("days_complete", 0)
    days_left    = current_cdd.get("days_remaining", 0)
    days_total   = days_done + days_left

    # Forecast = seasonal average (most reliable estimate)
    kwh_mid = avg_kwh
    kwh_p10 = p10_kwh
    kwh_p90 = p90_kwh

    # Last year comparison
    ly_kwh  = billing.get(ly_ym, {}).get("kwh")
    ly_cost = billing.get(ly_ym, {}).get("cost")

    # Cost estimate
    rate_blended  = _blended_rate()
    demand_cost   = avg_demand * _RATE_DEMAND
    nac_cost      = _RATE_NAC * (days_total or 30)
    cost_mid      = _kwh_to_zar(kwh_mid, rate_blended) + demand_cost + nac_cost
    cost_p10      = _kwh_to_zar(kwh_p10, rate_blended) + demand_cost + nac_cost
    cost_p90      = _kwh_to_zar(kwh_p90, rate_blended) + demand_cost + nac_cost

    yoy_kwh_pct   = ((kwh_mid - ly_kwh)  / ly_kwh  * 100) if ly_kwh  else None
    yoy_cost_pct  = ((cost_mid - ly_cost) / ly_cost * 100) if ly_cost else None

    return {
        "period":             ym,
        "days_complete":      days_done,
        "days_remaining":     days_left,
        "cdd_actual":         round(cdd_actual, 1),
        "cdd_forecast":       round(cdd_forecast, 1),
        "cdd_total_estimate": round(cdd_total, 1),
        "baseline_years":     _BASELINE_YEARS,
        "baseline_samples":   bas["samples"],
        "forecast_kwh": {
            "p10": int(kwh_p10),
            "mid": int(kwh_mid),
            "p90": int(kwh_p90),
        },
        "forecast_cost_zar": {
            "p10":            round(cost_p10, 0),
            "mid":            round(cost_mid, 0),
            "p90":            round(cost_p90, 0),
            "consumption":    round(_kwh_to_zar(kwh_mid, rate_blended), 0),
            "demand":         round(demand_cost, 0),
            "avg_demand_kva": round(avg_demand, 0),
            "blended_rate":   round(rate_blended, 4),
        },
        "same_month_last_year": {
            "month":       ly_ym,
            "kwh":         int(ly_kwh) if ly_kwh else None,
            "cost_zar":    round(ly_cost, 0) if ly_cost else None,
            "yoy_kwh_pct": round(yoy_kwh_pct, 1) if yoy_kwh_pct is not None else None,
            "yoy_cost_pct": round(yoy_cost_pct, 1) if yoy_cost_pct is not None else None,
        },
        "narrative": _month_end_narrative(
            ym, kwh_mid, cost_mid, ly_kwh, ly_cost,
            yoy_kwh_pct, yoy_cost_pct, cdd_total, days_done, days_left,
        ),
    }


def _month_end_narrative(month, kwh, cost, ly_kwh, ly_cost,
                          yoy_kwh, yoy_cost, cdd, days_done, days_left) -> str:
    ly_yr  = int(month[:4]) - 1
    ly_mo  = month[5:7]
    parts = [
        f"Month-end forecast ({month}): {kwh:,.0f} kWh · R{cost:,.0f}.",
        f"Based on 3-year seasonal average ({', '.join(str(y) for y in _BASELINE_YEARS)}).",
    ]
    if yoy_kwh is not None:
        sign      = "↓" if yoy_kwh < 0 else "↑"
        cost_sign = "↓" if (yoy_cost or 0) < 0 else "↑"
        parts.append(
            f"vs {ly_yr}-{ly_mo} actual: "
            f"{sign}{abs(yoy_kwh):.1f}% kWh, {cost_sign}{abs(yoy_cost or 0):.1f}% cost."
        )
    if days_left > 0:
        parts.append(f"{days_left} days remain. Month CDD estimate: {cdd:.0f}.")
    return " ".join(parts)


# ─── 2. Annual Budget Forecast ───────────────────────────────────────────────

def annual_budget_forecast(target_year: int = None) -> Dict[str, Any]:
    """
    Project full-year electricity budget.

    Actuals: months already billed (bucket 6 data with full kWh).
    Forecast: seasonal 3-year average (2023–2025), with July tariff increase.
    Current partial month: handled as forecast (not yet reconciled in billing).

    Returns full month-by-month breakdown + totals vs last year.
    """
    from .kpi_engine import _fetch_billing_history

    today       = date.today()
    target_year = target_year or today.year
    ly          = target_year - 1
    cur_ym      = today.strftime("%Y-%m")

    billing  = _fetch_billing_history(months=60)  # 5 years
    baseline = _seasonal_kwh_baseline(billing)

    rate_pre  = _blended_rate()
    rate_post = _apply_tariff_increase(rate_pre, 7)  # July

    months_out: Dict[str, Dict] = {}
    kwh_actual = kwh_fore = cost_actual = cost_fore = 0.0
    kwh_ly = cost_ly = 0.0

    for mo in range(1, 13):
        ym    = f"{target_year}-{mo:02d}"
        ly_ym = f"{ly}-{mo:02d}"
        cal   = f"{mo:02d}"
        rate  = rate_post if mo >= 7 else rate_pre

        bas_month  = baseline.get(cal, {})
        avg_kwh    = bas_month.get("avg", 550_000.0)
        p10_kwh    = bas_month.get("p10", avg_kwh * 0.90)
        p90_kwh    = bas_month.get("p90", avg_kwh * 1.10)
        avg_demand = bas_month.get("avg_demand_kva", 1_200.0)

        demand_cost = avg_demand * _RATE_DEMAND
        nac_cost    = _RATE_NAC * 30.0

        # Determine if this month has reconciled actual billing data
        # We treat a month as "actual" if it's in billing AND it's a full past month
        # (NOT the current partial month)
        is_past_month    = date(target_year, mo, 1) < date(today.year, today.month, 1)
        has_billing_data = (ym in billing and
                            (billing[ym].get("kwh") or 0) > 400_000)

        if is_past_month and has_billing_data:
            # --- Actual (reconciled billing) ---
            kwh  = billing[ym]["kwh"]
            cost = billing[ym].get("cost") or (_kwh_to_zar(kwh, rate) + demand_cost + nac_cost)
            cdd  = None  # Already consumed — CDD immaterial
            months_out[ym] = {
                "kwh": int(kwh), "cost_zar": round(cost, 0),
                "cdd": cdd, "type": "actual",
                "avg_demand_kva": billing[ym].get("max_demand_kva"),
            }
            kwh_actual  += kwh
            cost_actual += cost

        else:
            # --- Forecast (current month or future) ---
            kwh  = avg_kwh
            cost = _kwh_to_zar(kwh, rate) + demand_cost + nac_cost
            months_out[ym] = {
                "kwh": int(kwh), "cost_zar": round(cost, 0),
                "kwh_p10": int(p10_kwh), "kwh_p90": int(p90_kwh),
                "type": "forecast_partial" if ym == cur_ym else "forecast",
                "rate_applied": "post-July (+12%)" if mo >= 7 else "current",
                "avg_demand_kva": round(avg_demand, 0),
            }
            kwh_fore  += kwh
            cost_fore += cost

        # Last year actuals
        if ly_ym in billing:
            kwh_ly  += billing[ly_ym].get("kwh",  0) or 0
            cost_ly += billing[ly_ym].get("cost", 0) or 0

    total_kwh  = kwh_actual + kwh_fore
    total_cost = cost_actual + cost_fore

    # P10/P90 uncertainty on forecast months
    fore_months  = [m for m, v in months_out.items() if "forecast" in v["type"]]
    if fore_months:
        all_stds = [baseline.get(m[5:7], {}).get("std", 30_000.0) for m in fore_months]
        kwh_uncertainty = sum(s ** 2 for s in all_stds) ** 0.5  # Quadrature sum
    else:
        kwh_uncertainty = 0.0

    yoy_kwh_pct  = ((total_kwh  - kwh_ly)  / kwh_ly  * 100) if kwh_ly  else None
    yoy_cost_pct = ((total_cost - cost_ly) / cost_ly * 100) if cost_ly else None

    return {
        "year":          target_year,
        "baseline_years": _BASELINE_YEARS,
        "forecast_method": "seasonality (3-year calendar-month average, 2023–2025)",
        "tariff_increase_pct": _TARIFF_INCREASE_PCT,
        "months":        months_out,
        "total_kwh": {
            "actual":   int(kwh_actual),
            "forecast": int(kwh_fore),
            "total":    int(total_kwh),
            "p10":      int(max(0, total_kwh - 1.28 * kwh_uncertainty)),
            "p90":      int(total_kwh + 1.28 * kwh_uncertainty),
        },
        "total_cost_zar": {
            "actual":   round(cost_actual, 0),
            "forecast": round(cost_fore, 0),
            "total":    round(total_cost, 0),
        },
        "vs_last_year": {
            "year":         ly,
            "total_kwh":    int(kwh_ly)  if kwh_ly  else None,
            "total_cost":   round(cost_ly, 0) if cost_ly else None,
            "yoy_kwh_pct":  round(yoy_kwh_pct,  1) if yoy_kwh_pct  is not None else None,
            "yoy_cost_pct": round(yoy_cost_pct, 1) if yoy_cost_pct is not None else None,
        },
        "budget_summary": _annual_budget_narrative(
            target_year, total_kwh, total_cost,
            kwh_ly, cost_ly, yoy_kwh_pct, yoy_cost_pct,
            len(fore_months),
        ),
    }


def _annual_budget_narrative(year, kwh, cost, ly_kwh, ly_cost,
                              yoy_kwh, yoy_cost, n_fore) -> str:
    lines = [f"{year} electricity budget forecast: {kwh:,.0f} kWh · R{cost:,.0f}."]
    if yoy_kwh is not None and ly_kwh:
        lines.append(
            f"vs {year-1} actual ({ly_kwh:,.0f} kWh · R{ly_cost:,.0f}): "
            f"{'↓' if yoy_kwh < 0 else '↑'}{abs(yoy_kwh):.1f}% kWh, "
            f"{'↓' if (yoy_cost or 0) < 0 else '↑'}{abs(yoy_cost or 0):.1f}% cost."
        )
    lines.append(
        f"{n_fore} months forecast via 3-year seasonal average (2023–2025). "
        f"12% July tariff increase applied from month 7."
    )
    return " ".join(lines)


# ─── 3. TOU Shift Analysis ───────────────────────────────────────────────────

def tou_shift_analysis() -> Dict[str, Any]:
    """
    Quantify the financial opportunity from shifting load to off-peak.

    Back-calculates monthly kWh per TOU period from CoCT billing costs ÷ tariff rates.
    Models Scenario A (conservative 10% peak shift) and Scenario B (aggressive 20%+10%).
    """
    from .kpi_engine import _fetch_billing_history

    billing = _fetch_billing_history(months=12)

    tou_months = {
        m: v for m, v in billing.items()
        if v.get("offpeak_kwh", 0) > 0 and v.get("total_kwh_tou", 0) > 0
    }

    if not tou_months:
        return {
            "status": "no_tou_data",
            "message": (
                "TOU kWh breakdown uses reconciled CoCT billing (typically 2–3 months lag). "
                "Opportunity estimated from total consumption using assumed TOU split."
            ),
            "opportunity_zar_monthly": _estimate_opportunity_from_total(billing),
            "opportunity_zar_annual":  _estimate_opportunity_from_total(billing) * 12,
        }

    recent = sorted(tou_months, reverse=True)[:3]
    op_kwh  = sum(tou_months[m]["offpeak_kwh"]   for m in recent) / len(recent)
    tot_kwh = sum(tou_months[m]["total_kwh_tou"] for m in recent) / len(recent)
    lsi     = op_kwh / tot_kwh * 100 if tot_kwh > 0 else None

    peak_diff  = _RATE_PEAK     - _RATE_OFFPEAK
    std_diff   = _RATE_STANDARD - _RATE_OFFPEAK

    shift_a     = tot_kwh * _TOU_PEAK_PCT * 0.10
    saving_a    = shift_a * peak_diff
    shift_b_pk  = tot_kwh * _TOU_PEAK_PCT     * 0.20
    shift_b_std = tot_kwh * _TOU_STANDARD_PCT * 0.10
    saving_b    = shift_b_pk * peak_diff + shift_b_std * std_diff

    return {
        "status":      "analysed",
        "data_months": recent,
        "current_tou_split": {
            "offpeak_kwh_monthly":  round(op_kwh,  0),
            "total_metered_kwh":    round(tot_kwh, 0),
            "load_shift_index_pct": round(lsi, 1) if lsi else None,
        },
        "rate_differentials": {
            "peak_vs_offpeak":    round(peak_diff, 4),
            "standard_vs_offpeak": round(std_diff,  4),
        },
        "scenario_a": {
            "description":       "Conservative: shift 10% of peak load → off-peak",
            "shift_kwh_monthly": round(shift_a, 0),
            "saving_zar_monthly": round(saving_a, 0),
            "saving_zar_annual":  round(saving_a * 12, 0),
            "actions": [
                "Pool/spa heaters: timer 22:00–05:00",
                "Laundry: shift overnight cycles to 22:00 start",
            ],
        },
        "scenario_b": {
            "description":       "Aggressive: shift 20% peak + 10% standard → off-peak",
            "shift_kwh_monthly": round(shift_b_pk + shift_b_std, 0),
            "saving_zar_monthly": round(saving_b, 0),
            "saving_zar_annual":  round(saving_b * 12, 0),
            "actions": [
                "Pool/spa heaters: timer 22:00–05:00",
                "Laundry + cold storage defrost: off-peak schedule",
                "HVAC pre-cooling 21:00–22:00 (thermal mass advantage)",
                "EV/equipment charging: off-peak timer",
            ],
        },
        "recommendation": (
            f"Scenario A: R{round(saving_a*12/1000):.0f}K/year — minimal change required. "
            f"Scenario B: R{round(saving_b*12/1000):.0f}K/year — BMS programming needed."
        ),
    }


def _estimate_opportunity_from_total(billing: Dict = None) -> float:
    if billing is None:
        from .kpi_engine import _fetch_billing_history
        billing = _fetch_billing_history(months=3)
    recent  = sorted(billing, reverse=True)[:3]
    avg_kwh = sum(billing[m].get("kwh", 0) or 0 for m in recent) / max(len(recent), 1)
    shift   = avg_kwh * _TOU_PEAK_PCT * 0.10
    return round(shift * (_RATE_PEAK - _RATE_OFFPEAK), 0)
