---
description: Monthly sustainability report — EarthCheck KPIs, carbon footprint, YoY comparison
---

# Monthly Sustainability Report Workflow
Runs on the 1st of each month. Delivers to Sustainability Officer and GM.

## Steps

// turbo
1. Call `get_electricity_consumption(point_id=8323, days=30)` for the prior month.

// turbo
2. Call `get_water_consumption(point_id=8323, days=30)` for the prior month.

// turbo
3. Call `get_gas_consumption(point_id=8323, days=30)` for the prior month.

// turbo
4. Call `calculate_carbon_footprint(point_id=8323, days=30)` for Scope 1+2 emissions.

// turbo
5. Call `year_on_year_comparison(point_id=8323, utility="all")` for prior month vs same month last year.

// turbo
6. Call `analyze_base_load(point_id=8323, utility="all", days=30)` for base load status.

// turbo
7. Call `get_cape_town_weather(days_back=30, days_forward=0)` for temperature context (explains seasonal variation).

8. Compile EarthCheck KPI table:
   - Electricity: total kWh, base load (kW), YoY change (%)
   - Water: total kL, base load (L/hr), YoY change (%), m³/guest night if occupancy available
   - Gas: total m³, base load (m³/hr), YoY change (%)
   - Carbon: Scope 2 (electricity), Scope 1 (gas), total kgCO₂e, ZAR carbon tax cost
   - Water benchmark band: Excellent / Satisfactory / High / Excessive

9. Identify top 3 sustainability insights for the month.

10. Identify any EarthCheck KPI trending outside benchmark bands.

11. Format as professional sustainability report:
    - Executive headline (one sentence)
    - EarthCheck KPI table
    - Carbon footprint summary with ZAR carbon tax cost
    - YoY trend analysis
    - Top 3 insights
    - Recommended actions
    - Subject: `[One & Only CPT] Sustainability Report — {Month} {Year}`
