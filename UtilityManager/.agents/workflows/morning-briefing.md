---
description: Chief Engineer daily morning briefing — anomalies, base loads, meter health
---

# Morning Briefing Workflow
Runs at 06:30 Monday–Friday. Delivers to Chief Engineer.

## Steps

// turbo
1. Call `detect_anomalies(point_id=8323, utility="all", days=1)` to surface overnight anomalies.

// turbo
2. Call `analyze_base_load(point_id=8323, utility="all", days=90)` to check overnight base loads vs 90-day baseline.

// turbo
3. Call `check_power_factor_risk(point_id=8323)` to verify PF status.

// turbo
4. Call `check_demand_overage(point_id=8323)` to check demand vs contracted limit.

// turbo
5. Call `get_cape_town_weather(days_back=1, days_forward=3)` for weather context.

6. Synthesise into a Chief Engineer daily brief:
   - **Overnight Summary** (00:00–06:00): Any anomalies? Base load status?
   - **Meter Health**: All meters reporting? Any gaps >2h?
   - **Power Factor**: Current status and trend
   - **Demand**: Current month peak vs contracted limit
   - **Today's Weather**: Temperature forecast — any expected HVAC demand spikes?
   - **Action Items**: Numbered list of any required investigations

7. Format as a clean, technical email with subject: `[One & Only CPT] Morning Utility Brief — {date}`
