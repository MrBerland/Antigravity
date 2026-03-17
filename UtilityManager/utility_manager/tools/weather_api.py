"""
Weather API Tools — Open-Meteo Integration
==========================================
Free, no API key required. Hourly historical data back to 1940.
Cape Town coordinates: lat=-33.9249, lon=18.4241
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests

log = logging.getLogger(__name__)

_CAPE_TOWN_LAT = -33.9249
_CAPE_TOWN_LON = 18.4241
_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

_WEATHER_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "precipitation",
    "wind_speed_10m",
    "wind_direction_10m",
    "cloud_cover",
    "surface_pressure",
]


def _fetch_archive(start_date: str, end_date: str) -> Dict:
    params = {
        "latitude": _CAPE_TOWN_LAT,
        "longitude": _CAPE_TOWN_LON,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(_WEATHER_VARS),
        "timezone": "Africa/Johannesburg",
    }
    try:
        resp = requests.get(_ARCHIVE_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc)}


def _fetch_forecast(forecast_days: int) -> Dict:
    params = {
        "latitude": _CAPE_TOWN_LAT,
        "longitude": _CAPE_TOWN_LON,
        "hourly": ",".join(_WEATHER_VARS),
        "forecast_days": min(forecast_days, 16),
        "timezone": "Africa/Johannesburg",
    }
    try:
        resp = requests.get(_FORECAST_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc)}


def _summarise_weather(hourly: Dict) -> Dict:
    """Compute daily summary statistics from hourly data."""
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    humidity = hourly.get("relative_humidity_2m", [])
    precip = hourly.get("precipitation", [])
    wind = hourly.get("wind_speed_10m", [])
    apparent = hourly.get("apparent_temperature", [])

    valid_temps = [t for t in temps if t is not None]
    valid_wind = [w for w in wind if w is not None]
    valid_humid = [h for h in humidity if h is not None]
    total_rain = sum(p for p in precip if p is not None)

    return {
        "period_hours": len(times),
        "temperature": {
            "min_c": round(min(valid_temps), 1) if valid_temps else None,
            "max_c": round(max(valid_temps), 1) if valid_temps else None,
            "avg_c": round(sum(valid_temps) / len(valid_temps), 1) if valid_temps else None,
        },
        "apparent_temperature": {
            "min_c": round(min(t for t in apparent if t is not None), 1) if any(t is not None for t in apparent) else None,
            "max_c": round(max(t for t in apparent if t is not None), 1) if any(t is not None for t in apparent) else None,
        },
        "humidity_avg_percent": round(sum(valid_humid) / len(valid_humid), 1) if valid_humid else None,
        "precipitation_total_mm": round(total_rain, 2),
        "wind_speed_avg_kmh": round(sum(valid_wind) / len(valid_wind), 1) if valid_wind else None,
        "wind_speed_max_kmh": round(max(valid_wind), 1) if valid_wind else None,
    }


def get_cape_town_weather(days_back: int = 30, days_forward: int = 14) -> Dict[str, Any]:
    """
    Retrieve Cape Town weather data — historical and forecast.

    Used to correlate utility consumption with weather conditions.
    Includes temperature, humidity, wind, precipitation, and apparent temperature.
    Data source: Open-Meteo (free, no API key, Africa/Johannesburg timezone).

    Args:
        days_back: Days of historical weather to retrieve (max 2 years recommended)
        days_forward: Days of weather forecast to retrieve (max 16)

    Returns:
        Historical summary stats, hourly time-series, and forecast data.
    """
    now = datetime.now()
    result = {
        "location": "Cape Town, South Africa",
        "coordinates": {"lat": _CAPE_TOWN_LAT, "lon": _CAPE_TOWN_LON},
        "timezone": "Africa/Johannesburg",
    }

    if days_back > 0:
        start = (now - timedelta(days=days_back)).strftime("%Y-%m-%d")
        # Archive API requires end date to be at least 2 days ago
        end = (now - timedelta(days=2)).strftime("%Y-%m-%d")
        hist = _fetch_archive(start, end)
        if "error" not in hist:
            result["historical"] = {
                "period": {"start": start, "end": end, "days": days_back},
                "summary": _summarise_weather(hist.get("hourly", {})),
                "hourly": hist.get("hourly", {}),
            }
        else:
            result["historical_error"] = hist["error"]

    if days_forward > 0:
        fcast = _fetch_forecast(days_forward)
        if "error" not in fcast:
            result["forecast"] = {
                "days": days_forward,
                "summary": _summarise_weather(fcast.get("hourly", {})),
                "hourly": fcast.get("hourly", {}),
            }
        else:
            result["forecast_error"] = fcast["error"]

    return result


def correlate_utility_with_weather(
    consumption_data: List[float],
    temperature_data: List[float],
    utility: str = "electricity",
) -> Dict[str, Any]:
    """
    Calculate the statistical correlation between utility consumption and temperature.

    Quantifies how strongly HVAC load tracks temperature (expected R² > 0.6 for
    electricity in a Cape Town hotel). Use to validate HVAC efficiency and
    identify weather-adjusted consumption anomalies.

    Args:
        consumption_data: List of consumption values (kWh, kL, or m³)
        temperature_data: List of corresponding temperature values (°C)
        utility: Name of the utility being correlated ('electricity', 'water', 'gas')

    Returns:
        Pearson correlation coefficient, R², and interpretation.
    """
    if not consumption_data or not temperature_data:
        return {"error": "Empty data — provide both consumption_data and temperature_data lists"}

    n = min(len(consumption_data), len(temperature_data))
    if n < 5:
        return {"error": f"Insufficient data points ({n}) — need at least 5 for correlation"}

    c = consumption_data[:n]
    t = temperature_data[:n]

    mean_c = sum(c) / n
    mean_t = sum(t) / n

    cov = sum((ci - mean_c) * (ti - mean_t) for ci, ti in zip(c, t)) / n
    std_c = (sum((ci - mean_c) ** 2 for ci in c) / n) ** 0.5
    std_t = (sum((ti - mean_t) ** 2 for ti in t) / n) ** 0.5

    if std_c == 0 or std_t == 0:
        return {"error": "Zero variance in data — cannot compute correlation"}

    pearson_r = cov / (std_c * std_t)
    r_squared = pearson_r ** 2

    if r_squared > 0.7:
        strength = "Strong"
        interpretation = f"{utility.capitalize()} consumption is strongly temperature-driven. Weather-adjusted baseline recommended."
    elif r_squared > 0.4:
        strength = "Moderate"
        interpretation = f"Moderate weather influence on {utility}. HVAC likely a significant driver but other factors present."
    else:
        strength = "Weak"
        interpretation = f"Weak weather correlation for {utility}. Consumption may be driven by occupancy or operational patterns more than temperature."

    return {
        "utility": utility,
        "data_points": n,
        "pearson_r": round(pearson_r, 4),
        "r_squared": round(r_squared, 4),
        "correlation_strength": strength,
        "interpretation": interpretation,
        "direction": "Positive (consumption rises with temperature)" if pearson_r > 0 else "Negative (consumption falls with temperature)",
    }
