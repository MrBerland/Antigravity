---
description: Identify ToU shift opportunities and tariff switching savings
---

# Tariff Optimisation Workflow
Run monthly or when triggered by a significant cost increase.

## Steps

// turbo
1. Call `get_time_of_use(point_id=8323, days=30)` to see the current Peak/Standard/Off-Peak split.

// turbo
2. Call `get_tariff_comparison(point_id=8323)` to see alternative tariff costs.

// turbo
3. Call `get_cost_analysis(point_id=8323, days=30)` for line-item cost breakdown.

// turbo
4. Call `analyze_consumption_patterns(point_id=8323, utility="electricity", days=90)` for hourly load profile.

// turbo
5. Call `get_cape_town_weather(days_back=90, days_forward=14)` for seasonal context.

6. Analyse ToU optimisation potential:
   - What % of consumption falls in Peak periods? (Target: minimise)
   - What loads are shiftable to Off-Peak? (Laundry, pool plant, EV charging, pre-cooling)
   - What is the ZAR savings potential if 10%/20%/30% of Peak load is shifted?

7. Analyse tariff switching:
   - Does an alternative tariff offer a lower blended rate?
   - What is the 12-month cost delta?
   - Are there exit clauses or minimum contract terms on current tariff?

8. Calculate demand management opportunities:
   - Can HVAC staggered startup avoid a demand spike at 07:00?
   - What is the ZAR saving if demand is reduced by 50kVA / 100kVA?

9. Generate optimisation report for Financial Controller + Chief Engineer:
   - Current ToU split (peak/standard/off-peak %)
   - Tariff switching analysis (current vs best alternative)
   - Top 3 actionable cost reduction opportunities with ZAR values
   - Required capital investment for each opportunity (if applicable)
   - Payback period estimate
