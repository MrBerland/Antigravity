---
description: P1 Critical — suspected water leak detected overnight. Immediate response protocol.
---

# Water Leak Response Workflow
Triggered when water base load exceeds 200 L/hr between 02:00–05:00.
This is a P1 Critical alert — time-sensitive.

## Steps

// turbo
1. Call `analyze_base_load(point_id=8323, utility="water", days=30)` to quantify the leak: current flow vs 30d baseline.

// turbo
2. Call `get_water_consumption(point_id=8323, days=7)` to identify when the leak started (first elevated overnight reading).

// turbo
3. Call `get_all_utility_consumption(point_id=8323, days=1)` to check if electricity or gas also changed (could indicate pump/boiler fault).

4. Calculate estimated leak volume:
   - Flow rate above baseline (L/hr)
   - Hours of anomalous flow
   - Total estimated volume lost (kL)
   - Estimated cost at current water tariff (ZAR)

5. Identify sub-meter context: If sub-meters are available, identify which circuit is elevated.

6. Generate an immediate P1 alert for Chief Engineer containing:
   - **Alert:** Suspected water leak detected
   - **Estimated flow rate:** X L/hr above normal base load
   - **Estimated volume lost:** X kL since {start_time}
   - **Estimated cost:** ZAR X
   - **Leak started:** Approximately {timestamp}
   - **Affected area:** {sub-meter name if available}
   - **Recommended action:** Immediate physical inspection of [areas]

7. Log the event in memory/anomaly_log.json for audit purposes.
