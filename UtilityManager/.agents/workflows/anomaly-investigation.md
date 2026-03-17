---
description: Investigate a detected anomaly — root cause analysis and recommended action
---

# Anomaly Investigation Workflow
Triggered automatically when a P1 or P2 anomaly is detected.

## Steps

1. Identify the anomaly details: utility, magnitude, time window, affected meters.

// turbo
2. Call `get_all_utility_consumption(point_id=8323, days=7)` to see cross-utility context around the anomaly window.

// turbo
3. Call `get_cape_town_weather(days_back=7, days_forward=0)` to check if weather explains the anomaly.

// turbo
4. Call `analyze_consumption_patterns(point_id=8323, utility=<affected_utility>, days=90)` to compare against seasonal baseline.

// turbo
5. Call `get_technical_analysis(point_id=8323, days=3)` for phase-level detail if anomaly is electrical.

6. Cross-reference results:
   - Is the anomaly explained by weather (e.g., heatwave → AC spike)?
   - Is it explained by occupancy patterns (e.g., event in house)?
   - Is it explained by a meter fault (e.g., erratic readings)?
   - Is it a genuine operational issue requiring action?

7. Classify the outcome:
   - **False Positive** — document reason, adjust threshold if needed
   - **Explained** — document cause (weather/event), no action required
   - **Genuine Anomaly** — generate action item for Chief Engineer
   - **Equipment Fault** — immediate escalation to engineering team

8. Output a structured anomaly investigation report:
   - Anomaly summary
   - Root cause assessment
   - Supporting evidence (data, weather, baseline comparison)
   - Recommended action
   - Priority (P1/P2/P3)
