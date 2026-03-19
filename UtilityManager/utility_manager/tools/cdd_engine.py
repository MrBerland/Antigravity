"""
CDD Engine — Cooling & Heating Degree Days + EnPI Regression
=============================================================
Provides:
  - Monthly CDD/HDD series from Open-Meteo historical data
  - EnPI linear regression (kWh ~ CDD) with R² and coefficients
  - Weather-normalised consumption (actual vs EnPI-predicted)
  - Today's CDD-to-date + forecast CDD for remainder of month

CDD base: 18°C  (South African commercial buildings standard)
HDD base: 15°C  (Cape Town mild winters — boiler / heat pump driver)

Used by: kpi_engine.py, forecasting_engine.py, anomaly_detection.py
"""

import logging
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

import requests

log = logging.getLogger(__name__)

_ARCHIVE_URL  = "https://archive-api.open-meteo.com/v1/archive"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

CDD_BASE = 18.0   # °C — cooling begins above this
HDD_BASE = 15.0   # °C — heating begins below this
_TZ      = "Africa/Johannesburg"


# ─── Raw daily temperature from Open-Meteo ──────────────────────────────────

def _fetch_daily_temps(start: str, end: str, lat: float, lon: float) -> Dict:
    """Pull daily mean/max/min temperature from Open-Meteo archive."""
    try:
        r = requests.get(_ARCHIVE_URL, params={
            "latitude": lat, "longitude": lon,
            "start_date": start, "end_date": end,
            "daily": "temperature_2m_mean,temperature_2m_max,temperature_2m_min",
            "timezone": _TZ,
        }, timeout=30)
        r.raise_for_status()
        return r.json().get("daily", {})
    except Exception as e:
        log.warning("CDD archive fetch failed: %s", e)
        return {}


def _fetch_forecast_temps(days: int, lat: float, lon: float) -> Dict:
    """Pull forecast daily mean temperature from Open-Meteo."""
    try:
        r = requests.get(_FORECAST_URL, params={
            "latitude": lat, "longitude": lon,
            "daily": "temperature_2m_mean,temperature_2m_max,temperature_2m_min",
            "forecast_days": min(days, 16),
            "timezone": _TZ,
        }, timeout=30)
        r.raise_for_status()
        return r.json().get("daily", {})
    except Exception as e:
        log.warning("CDD forecast fetch failed: %s", e)
        return {}


# ─── Degree Day calculation ──────────────────────────────────────────────────

def _daily_cdd_hdd(mean_temp: float) -> Tuple[float, float]:
    """Return (CDD, HDD) for a single day given mean temperature."""
    cdd = max(0.0, mean_temp - CDD_BASE)
    hdd = max(0.0, HDD_BASE - mean_temp)
    return round(cdd, 2), round(hdd, 2)


def get_monthly_cdd_series(
    lat: float, lon: float,
    start_year: int = 2021,
    start_month: int = 1,
) -> Dict[str, Dict]:
    """
    Build a monthly CDD and HDD series from start_year/month to last month.

    Returns:
        Dict keyed "YYYY-MM" → {cdd, hdd, avg_temp, days}

    Example:
        {"2024-01": {"cdd": 187.4, "hdd": 0.0, "avg_temp": 24.3, "days": 31}, ...}
    """
    today = date.today()
    # End at last fully-completed month
    if today.month == 1:
        end_year, end_month = today.year - 1, 12
    else:
        end_year, end_month = today.year, today.month - 1

    start_date = date(start_year, start_month, 1).strftime("%Y-%m-%d")
    end_date   = date(end_year, end_month,
                      _days_in_month(end_year, end_month)).strftime("%Y-%m-%d")

    log.info("Fetching daily temps %s → %s for CDD series", start_date, end_date)
    daily = _fetch_daily_temps(start_date, end_date, lat, lon)

    if not daily.get("time"):
        log.warning("No daily temperature data returned — empty CDD series")
        return {}

    # Aggregate by month
    series: Dict[str, Dict] = {}
    for dt_str, mean_t in zip(daily["time"], daily.get("temperature_2m_mean", [])):
        if mean_t is None:
            continue
        ym = dt_str[:7]  # "YYYY-MM"
        if ym not in series:
            series[ym] = {"cdd": 0.0, "hdd": 0.0, "temp_sum": 0.0, "days": 0}
        cdd, hdd = _daily_cdd_hdd(mean_t)
        series[ym]["cdd"]      += cdd
        series[ym]["hdd"]      += hdd
        series[ym]["temp_sum"] += mean_t
        series[ym]["days"]     += 1

    # Finalise averages
    result = {}
    for ym, v in sorted(series.items()):
        result[ym] = {
            "cdd":      round(v["cdd"], 1),
            "hdd":      round(v["hdd"], 1),
            "avg_temp": round(v["temp_sum"] / v["days"], 1) if v["days"] else None,
            "days":     v["days"],
        }
    return result


def get_current_month_cdd(lat: float, lon: float) -> Dict:
    """
    Return CDD accumulated so far this month + forecast for remainder.

    Returns:
        {
          "month": "2026-03",
          "cdd_actual": 24.3,    # CDD accumulated days 1 → yesterday
          "cdd_forecast": 18.7,  # CDD forecast days today → end of month
          "cdd_total_estimate": 43.0,
          "days_complete": 18,
          "days_remaining": 13,
        }
    """
    today = date.today()
    ym    = today.strftime("%Y-%m")
    month_start = date(today.year, today.month, 1)
    yesterday   = today - timedelta(days=1)

    result: Dict = {"month": ym}

    # --- Actual CDD so far this month ---
    if yesterday >= month_start:
        daily_hist = _fetch_daily_temps(
            month_start.strftime("%Y-%m-%d"),
            yesterday.strftime("%Y-%m-%d"),
            lat, lon,
        )
        cdd_actual = 0.0
        days_done  = 0
        for mean_t in daily_hist.get("temperature_2m_mean", []):
            if mean_t is not None:
                cdd_actual += max(0.0, mean_t - CDD_BASE)
                days_done  += 1
        result["cdd_actual"]   = round(cdd_actual, 1)
        result["days_complete"] = days_done
    else:
        result["cdd_actual"]    = 0.0
        result["days_complete"] = 0

    # --- Forecast CDD for rest of month ---
    days_left = _days_in_month(today.year, today.month) - today.day + 1
    daily_fcast = _fetch_forecast_temps(days_left, lat, lon)
    cdd_fcast   = 0.0
    for mean_t in daily_fcast.get("temperature_2m_mean", []):
        if mean_t is not None:
            cdd_fcast += max(0.0, mean_t - CDD_BASE)
    result["cdd_forecast"]       = round(cdd_fcast, 1)
    result["days_remaining"]     = days_left
    result["cdd_total_estimate"] = round(result["cdd_actual"] + cdd_fcast, 1)

    return result


# ─── EnPI Regression ─────────────────────────────────────────────────────────

def fit_enpi_model(
    monthly_kwh: Dict[str, float],
    monthly_cdd: Dict[str, Dict],
) -> Dict:
    """
    Fit a linear EnPI model: monthly_kWh = α + β × monthly_CDD

    Args:
        monthly_kwh: {"YYYY-MM": kWh} — from billing history
        monthly_cdd: {"YYYY-MM": {"cdd": float, ...}} — from get_monthly_cdd_series()

    Returns:
        {
          "alpha": float,         # intercept (base load component, kWh/month)
          "beta": float,          # CDD coefficient (kWh per degree-day)
          "r_squared": float,     # model fit quality (target > 0.65)
          "n_months": int,
          "interpretation": str,
          "monthly_residuals": {"YYYY-MM": residual_kwh},
          "monthly_predicted": {"YYYY-MM": predicted_kwh},
        }
    """
    # Find months where both kWh and CDD are available
    common_months = sorted(set(monthly_kwh) & set(monthly_cdd))
    pairs = [(monthly_cdd[m]["cdd"], monthly_kwh[m]) for m in common_months
             if monthly_cdd[m]["cdd"] is not None and monthly_kwh[m] > 0]

    if len(pairs) < 6:
        return {
            "error": f"Insufficient paired data ({len(pairs)} months). Need ≥6.",
            "n_months": len(pairs),
        }

    n   = len(pairs)
    xs  = [p[0] for p in pairs]   # CDD values
    ys  = [p[1] for p in pairs]   # kWh values
    mx  = sum(xs) / n
    my  = sum(ys) / n

    # OLS regression
    ss_xy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    ss_xx = sum((x - mx) ** 2 for x in xs)

    if ss_xx == 0:
        return {"error": "No variance in CDD — cannot fit model (all months same CDD)"}

    beta  = ss_xy / ss_xx
    alpha = my - beta * mx

    # R²
    ss_res = sum((y - (alpha + beta * x)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2     = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    # Residuals and predictions per month
    residuals  = {}
    predicted  = {}
    for m, (cdd_val, kwh_val) in zip(common_months, pairs):
        pred = alpha + beta * cdd_val
        residuals[m]  = round(kwh_val - pred, 0)
        predicted[m]  = round(pred, 0)

    # Interpretation
    if r2 > 0.75:
        interp = (f"Strong climate-energy relationship (R²={r2:.2f}). "
                  f"Temperature explains {r2*100:.0f}% of monthly consumption variance. "
                  f"Climate is the primary EnPI driver for this site.")
    elif r2 > 0.50:
        interp = (f"Moderate climate-energy relationship (R²={r2:.2f}). "
                  f"Temperature explains {r2*100:.0f}% of variance. "
                  f"Occupancy or operational factors also significant.")
    else:
        interp = (f"Weak climate-energy relationship (R²={r2:.2f}). "
                  f"Consumption is driven primarily by factors other than temperature. "
                  f"Review occupancy patterns, operational changes, or major load additions.")

    return {
        "alpha":             round(alpha, 0),
        "beta":              round(beta, 1),
        "r_squared":         round(r2, 3),
        "n_months":          n,
        "mean_monthly_kwh":  round(my, 0),
        "mean_cdd":          round(mx, 1),
        "interpretation":    interp,
        "monthly_residuals": residuals,
        "monthly_predicted": predicted,
        "months_used":       common_months,
    }


def predict_kwh(model: Dict, cdd: float) -> Optional[float]:
    """
    Predict kWh consumption for a given CDD value using a fitted EnPI model.

    Returns None if model has an error.
    """
    if "error" in model:
        return None
    return round(model["alpha"] + model["beta"] * cdd, 0)


def weather_normalised_variance(
    actual_kwh: float,
    model: Dict,
    cdd: float,
) -> Dict:
    """
    Compare actual consumption to what the EnPI model predicts for a given CDD.

    Returns:
        {
          "actual_kwh": float,
          "predicted_kwh": float,
          "variance_kwh": float,       # positive = overdraw vs climate expectation
          "variance_pct": float,
          "interpretation": str,
        }
    """
    predicted = predict_kwh(model, cdd)
    if predicted is None:
        return {"error": "No valid EnPI model"}

    var_kwh = actual_kwh - predicted
    var_pct = (var_kwh / predicted * 100) if predicted else 0.0

    if abs(var_pct) < 5:
        interp = "Within normal range (±5% of climate expectation)."
    elif var_pct > 0:
        interp = (f"Consuming {var_pct:.1f}% MORE than expected for this weather. "
                  f"Investigate non-climate loads or efficiency degradation.")
    else:
        interp = (f"Consuming {abs(var_pct):.1f}% LESS than expected for this weather. "
                  f"Efficiency improvement confirmed — good performance.")

    return {
        "actual_kwh":    round(actual_kwh, 0),
        "predicted_kwh": round(predicted, 0),
        "variance_kwh":  round(var_kwh, 0),
        "variance_pct":  round(var_pct, 1),
        "interpretation": interp,
    }


# ─── Utility ─────────────────────────────────────────────────────────────────

def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        return 31
    return (date(year, month + 1, 1) - date(year, month, 1)).days
