"""
Augos Intelligence — Web Dashboard
====================================
Flask server with in-memory TTL cache.
First load: slow (live API calls). Subsequent: instant (5-min cache).

Run: python3 web/app.py
Access: http://localhost:5050
"""

import json
import os
import sys
import logging
import time
from datetime import datetime
from pathlib import Path
from threading import Lock
from functools import wraps

sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from flask import Flask, jsonify, render_template

log = logging.getLogger(__name__)
app = Flask(__name__)

# ─── Simple TTL cache ─────────────────────────────────────────────────────────

_CACHE: dict = {}
_LOCK  = Lock()
CACHE_TTL = 300  # 5 minutes

def cached(key: str, fn, ttl: int = CACHE_TTL):
    with _LOCK:
        if key in _CACHE:
            ts, val = _CACHE[key]
            if time.time() - ts < ttl:
                log.info("Cache HIT: %s", key)
                return val
    log.info("Cache MISS: %s — computing...", key)
    try:
        val = fn()
    except Exception as e:
        log.error("Error computing %s: %s", key, e, exc_info=True)
        val = {"error": str(e)}
    with _LOCK:
        _CACHE[key] = (time.time(), val)
    return val

# ─── API Endpoints ────────────────────────────────────────────────────────────

@app.route("/api/kpis")
def api_kpis():
    def _compute():
        from utility_manager.tools.kpi_engine import compute_kpis
        return compute_kpis(months=3)
    return jsonify(cached("kpis", _compute))


@app.route("/api/baseload")
def api_baseload():
    def _compute():
        # Use billing history for base load trend (fast, no high-res data needed)
        from utility_manager.tools.kpi_engine import _fetch_billing_history
        billing = _fetch_billing_history(months=36)
        # Build monthly kWh sorted series for trend analysis
        months = sorted([
            {"month": m, "kwh": d["kwh"], "cost": d.get("cost", 0),
             "peak_kva": d.get("max_demand_kva")}
            for m, d in billing.items()
            if (d.get("kwh") or 0) > 400_000
        ], key=lambda x: x["month"])

        if not months:
            return {"error": "No billing data available"}

        kwh_vals = [m["kwh"] for m in months]
        mean_kwh = sum(kwh_vals) / len(kwh_vals)
        # Estimate base load as ~80% of minimum monthly (always-on portion)
        min_kwh  = min(kwh_vals)
        baseload_kw_est = (min_kwh * 0.80) / (30 * 24)  # kW equivalent
        max_kw   = (max(kwh_vals) * 0.80) / (30 * 24)

        # Trend: compare first 6 months vs last 6
        first6 = sum(kwh_vals[:6]) / 6 if len(kwh_vals) >= 6 else kwh_vals[0]
        last6  = sum(kwh_vals[-6:]) / 6 if len(kwh_vals) >= 6 else kwh_vals[-1]
        trend_pct = (last6 - first6) / first6 * 100 if first6 else 0

        return {
            "status": "ok",
            "monthly_series": months,
            "base_load": {
                "electricity": {
                    "status":         "analysed",
                    "mean":           round(baseload_kw_est, 1),
                    "min":            round(baseload_kw_est * 0.85, 1),
                    "max":            round(max_kw, 1),
                    "trend_percent":  round(trend_pct, 1),
                    "trend_direction": "rising" if trend_pct > 5 else "falling" if trend_pct < -5 else "stable",
                    "window":         "02:00–05:00 (estimated from monthly min)",
                    "assessment":     "P2_WARNING" if trend_pct > 10 else "normal",
                    "flags": [f"Base load rising {trend_pct:.1f}% over period"] if trend_pct > 10 else [],
                }
            }
        }
    return jsonify(cached("baseload", _compute))


@app.route("/api/enpi")
def api_enpi():
    def _compute():
        from utility_manager.tools.kpi_engine import _fetch_billing_history
        from utility_manager.tools.cdd_engine import get_monthly_cdd_series, fit_enpi_model

        lat = float(os.getenv("SITE_LAT", "-33.9249"))
        lon = float(os.getenv("SITE_LON", "18.4241"))
        billing  = _fetch_billing_history(months=36)
        cdd_data = get_monthly_cdd_series(lat, lon)
        monthly_kwh = {m: billing[m]["kwh"] for m in billing if billing[m].get("kwh", 0) > 0}
        model = fit_enpi_model(monthly_kwh, cdd_data)

        common = sorted(set(monthly_kwh) & set(cdd_data))
        points = []
        for m in common:
            cdd = cdd_data[m].get("cdd", 0)
            kwh = monthly_kwh.get(m, 0)
            if kwh > 400_000:
                pred     = model.get("monthly_predicted", {}).get(m)
                residual = model.get("monthly_residuals", {}).get(m)
                points.append({
                    "month":    m,
                    "cdd":      round(cdd, 1),
                    "kwh":      round(kwh, 0),
                    "predicted": round(pred, 0) if pred else None,
                    "residual":  round(residual, 0) if residual else None,
                    "year":     int(m[:4]),
                })

        return {
            "model": {
                "alpha":     round(model.get("alpha", 0), 0),
                "beta":      round(model.get("beta", 0), 2),
                "r_squared": model.get("r_squared", 0),
            },
            "scatter": points,
            "residuals": [
                {"month": m, "residual": round(r, 0)}
                for m, r in sorted(model.get("monthly_residuals", {}).items())
                if m in {p["month"] for p in points}
            ],
        }
    return jsonify(cached("enpi", _compute))


@app.route("/api/billing-history")
def api_billing_history():
    def _compute():
        from utility_manager.tools.kpi_engine import _fetch_billing_history
        billing = _fetch_billing_history(months=36)
        rows = sorted([
            {"month": m, "kwh": round(d.get("kwh", 0), 0),
             "cost": round(d.get("cost", 0), 0),
             "peak_kva": d.get("max_demand_kva")}
            for m, d in billing.items()
            if (d.get("kwh") or 0) > 400_000
        ], key=lambda x: x["month"])
        return {"months": rows}
    return jsonify(cached("billing", _compute))


@app.route("/api/forecast")
def api_forecast():
    def _compute():
        from utility_manager.tools.forecasting_engine import month_end_forecast, annual_budget_forecast
        return {"month_end": month_end_forecast(), "annual": annual_budget_forecast()}
    return jsonify(cached("forecast", _compute))


@app.route("/api/events")
def api_events():
    def _compute():
        from utility_manager.tools.email_reader import get_recent_report_emails
        emails = get_recent_report_emails(days_back=7, max_results=30)
        return {"events": [
            {"date": e.get("date",""), "persona": e.get("persona",""),
             "subject": e.get("subject",""), "critical": e.get("critical_count",0),
             "warnings": e.get("warning_count",0), "all_clear": e.get("all_clear",False)}
            for e in emails
        ]}
    return jsonify(cached("events", _compute, ttl=120))  # 2-min cache for events


@app.route("/api/anomalies")
def api_anomalies():
    def _compute():
        from utility_manager.tools.anomaly_detection import detect_enpi_anomalies
        findings = detect_enpi_anomalies(months_to_check=6)
        return {"findings": findings, "count": len(findings)}
    return jsonify(cached("anomalies", _compute))


@app.route("/api/cache/clear")
def api_cache_clear():
    with _LOCK:
        _CACHE.clear()
    return jsonify({"status": "cache cleared"})


# ─── Main page ────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html",
                           now=datetime.now().strftime("%A, %-d %B %Y · %H:%M"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")
    print("\n🔋 Augos Intelligence Dashboard")
    print("   http://localhost:5050")
    print("   First load is slow (live API calls). Refresh is instant (5-min cache).\n")
    app.run(host="0.0.0.0", port=5050, debug=False, threaded=True)
