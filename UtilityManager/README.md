# Utility Manager Agent
## Hotel Utility Intelligence for One & Only Cape Town

A specialist AI agent monitoring **Electricity · Water · Gas** via the Augos platform.
Delivers anomaly detection, weather correlations, EarthCheck KPI reporting, and
cost optimisation insights — completely standalone from any other project.

---

## Quick Start

```bash
# 1. Clone / navigate to project
cd /Users/timstevens/Antigravity/UtilityManager

# 2. Set up environment
cp .env.example .env
# Edit .env — add AUGOS_EMAIL, AUGOS_PASSWORD (and email recipients)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the agent
./run.sh
# or: adk web
```

Open the ADK web interface at http://localhost:8000

---

## Project Structure

```
UtilityManager/
├── utility_manager/          ← ADK agent package (discovered by `adk web`)
│   ├── agent.py              ← Root agent + full system instructions
│   ├── __init__.py
│   └── tools/
│       ├── auth_manager.py   ← Smart session caching (≤48 logins/day)
│       ├── augos_api.py      ← All 13 Augos endpoints (elec + water + gas)
│       ├── weather_api.py    ← Open-Meteo integration (Cape Town)
│       ├── anomaly_detection.py ← Z-score engine + hotel-specific rules
│       ├── pattern_analysis.py  ← Patterns, forecasting, carbon, YoY
│       └── __init__.py       ← Tool registry
├── .agents/workflows/        ← Reusable agent workflows
│   ├── morning-briefing.md
│   ├── anomaly-investigation.md
│   ├── water-leak-response.md
│   ├── monthly-sustainability-report.md
│   └── tariff-optimisation.md
├── knowledge/                ← Agent knowledge base
│   ├── hotel-profile.md
│   ├── earthcheck-framework.md
│   ├── tariff-context.md
│   └── sustainability-goals.md
├── config/                   ← Configuration
│   ├── hotels.yaml           ← Hotel registry (add new properties here)
│   ├── thresholds.yaml       ← Anomaly thresholds
│   ├── product_types.yaml    ← Augos productTypeID mapping
│   └── emission_factors.yaml ← Carbon emission factors (SA 2025)
├── memory/                   ← Runtime state (token cache, logs)
├── .env.example              ← Environment template
├── requirements.txt
└── run.sh                    ← Start script
```

---

## Authentication

Uses programmatic login (`POST /api/auth/login`) with a **persistent token cache**.

| Constraint | Value |
|-----------|-------|
| API Login Limit | 48 per 24 hours |
| Agent Target | ≤ 3 logins/day |
| Token Max Age | 20 hours (refreshed before expiry) |
| Cache Location | `memory/token_cache.json` |

Set `AUGOS_EMAIL` and `AUGOS_PASSWORD` in `.env`.

---

## Available Tools (26 total)

### Augos API (16 tools)
| Tool | Description |
|------|-------------|
| `resolve_site` | Search hotel by name → Point ID |
| `get_site_overview` | Site metadata & hierarchy |
| `get_electricity_consumption` | Electricity (kWh) with sub-meter breakdown |
| `get_water_consumption` | Water (kL) — productTypeID auto-discovered |
| `get_gas_consumption` | Gas (m³) — productTypeID auto-discovered |
| `get_all_utility_consumption` | All 3 utilities in one call |
| `get_dashboard` | KPI summary cards |
| `get_cost_analysis` | Tariff line items in ZAR |
| `get_bill_verification` | Calculated vs billed comparison |
| `get_cost_allocation` | Cost distribution by cost centre |
| `get_tariff_comparison` | Current vs alternative tariff costs |
| `get_power_factor` | PF trend + max demand + penalty risk |
| `get_time_of_use` | Peak/Standard/Off-Peak split |
| `get_technical_analysis` | Interval data + phase readings |
| `get_live_curtailment_status` | Real-time CBL compliance |
| `get_sensor_readings` | S&M module sensor data |

### Weather (2 tools)
| Tool | Description |
|------|-------------|
| `get_cape_town_weather` | Historical + 16-day forecast (Open-Meteo) |
| `correlate_utility_with_weather` | Pearson R, R², interpretation |

### Anomaly Detection (4 tools)
| Tool | Description |
|------|-------------|
| `detect_anomalies` | Z-score anomaly detection (all utilities) |
| `analyze_base_load` | 02:00–05:00 base load analysis + leak detection |
| `check_power_factor_risk` | PF penalty risk + severity classification |
| `check_demand_overage` | Peak demand vs contracted limit |

### Pattern Analysis & Intelligence (4 tools)
| Tool | Description |
|------|-------------|
| `analyze_consumption_patterns` | Statistics, trends, seasonal context |
| `forecast_consumption` | 30-day exponential smoothing forecast |
| `year_on_year_comparison` | Current month vs same month prior year |
| `identify_savings_opportunities` | Ranked ZAR savings opportunities |
| `calculate_carbon_footprint` | Scope 1+2 kgCO₂e + ZAR carbon tax |

---

## Personas & Email Schedule

| Persona | Schedule | Content |
|---------|----------|---------|
| Chief Engineer | Daily 06:30 Mon–Fri | Anomalies, base loads, meter health, PF |
| Chief Engineer | Weekly Mon 07:00 | Technical summary, PF trend, demand |
| General Manager | Weekly Mon 08:00 | Executive snapshot, top 3 insights |
| General Manager | Monthly 1st | Full narrative report |
| Financial Controller | Monthly 1st | Cost breakdown, bill verification, ToU |
| Sustainability Officer | Monthly 1st | EarthCheck KPIs, carbon, YoY comparison |
| Sustainability Officer | Quarterly | Benchmarking, Green Star metrics |

### Anomaly Alert Routing
| Severity | Trigger | Recipients |
|----------|---------|-----------|
| P1 Critical | Water leak, meter outage, demand breach, PF < 0.90 | Engineer + GM |
| P2 Warning | PF < 0.92, spike > 30%, rising base load | Chief Engineer |
| P3 Insight | Tariff opportunity, record demand, KPI band change | Finance + GM (next report) |

---

## EarthCheck KPIs Tracked

| KPI | Unit | Benchmark (Mediterranean) |
|-----|------|--------------------------|
| Electricity base load | kW (02:00–05:00) | <25% of daytime peak |
| Water intensity | m³/guest night* | Excellent <0.60 |
| Water base load | L/hr (02:00–05:00) | <50 L/hr (leak signal) |
| Gas base load | m³/hr (00:00–05:00) | Derived from baseline |
| Scope 2 emissions | kgCO₂e | YoY reduction target |
| Scope 1 emissions | kgCO₂e | YoY reduction target |
| Carbon tax exposure | ZAR | Minimise |

*Occupancy hook built in — activate by providing `OCCUPANCY_DATA_SOURCE` in future.

---

## Adding More Hotels

Edit `config/hotels.yaml` — add a new entry following the One & Only pattern.
The agent supports multi-property benchmarking natively.

---

## Deployment to Vertex AI

```bash
gcloud auth login
gcloud config set project augos-core-data
adk deploy --project=augos-core-data --region=us-central1
```

---

*Utility Manager Agent · Standalone project · Not part of HiveMind*  
*Built: March 2026 · One & Only Cape Town · Augos Point ID: 8323*
