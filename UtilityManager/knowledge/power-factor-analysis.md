# Power Factor Analysis — Knowledge Base
## One & Only Cape Town | Augos Data Format + CoCT Context

---

## Site Architecture
The site (Point ID: 8323) is a **virtual aggregation meter**. Power Factor is NOT
meaningful at the virtual site level — it averages across the two independent
PFC systems and masks real issues.

**Always analyse PF at the next level down:**
| Point | Label | PFC System | kVA (peak observed) |
|---|---|---|---|
| 8324 | Main Switch 1 | PFC-A | 775 kVA (Jan 26) |
| 8336 | Main Switch 2 | PFC-B | 604 kVA (Dec 25) |

---

## Augos API — Power Factor Data Format

**Endpoint:** `GET /api/v1/power-factor-demand`  
**Parameters:** `pointID`, `startDateUTC`, `endDateUTC`

**Response structure (pivot table — not a list):**
```json
{
  "tariffReportID": 12345,
  "details": [
    {"itemsDescription": "actualDemand", "Mar 26": 1085.6, "Feb 26": 1131.4, ...},
    {"itemsDescription": "actualkVAR",   "Mar 26": 266.7,  "Feb 26": 329.4,  ...},
    {"itemsDescription": "actualPf",     "Mar 26": 0.9693, "Feb 26": 0.9567, ...},
    {"itemsDescription": "actualPower",  "Mar 26": 1052.4, "Feb 26": 1082.4, ...}
  ]
}
```
Month keys format: `"Mon YY"` (e.g. "Mar 26", "Feb 26"). Skip keys:
`index`, `pointID`, `point`, `parentID`, `itemsDescription`, `total`.

---

## Financial Impact Methodology

**The demand charge is billed on kVA (not kW).** Every reduction in kVA directly
reduces the demand charge.

**Observed rates (March 2026 billing):**
- Demand charge: R345,084 for 1,085.7 kVA peak → **~R318/kVA/month**  
  *(Note: verify this rate each billing cycle — it changes with CoCT tariff review)*

**Saving calculation per month:**
```
excess_kVA = kVA_actual - (kW / pf_target)
monthly_saving = excess_kVA × demand_rate_zar_per_kva
```

**PF correction target:** Always calculate to PF 0.99 (realistic well-maintained PFC),
not just to 0.95 (the penalty threshold). The full benefit is in the full correction.

---

## Two-Year Historical Findings (Apr 2024 – Mar 2026)

### Main Switch 1 (PFC-A) — Problem System
| Month | PF | kVA | Status |
|---|---|---|---|
| Nov 2024 | 0.9295 | 623 kVA | 🟡 Below 0.95 |
| Jan 2026 | 0.9381 | 775 kVA (PEAK) | 🟡 Below 0.95 + High Demand |
| Feb 2026 | 0.9338 | 723 kVA | 🟡 Below 0.95 + High Demand |
| Dec 2025 | 0.9587 | 770 kVA | 👀 Watch — near threshold |
| Feb 2025 | 0.9606 | 665 kVA | 👀 Watch — near threshold |
| Mar 2026 | 0.9591 | 677 kVA | 👀 Watch — near threshold |

**Pattern:** PF degrades Nov–Mar (southern hemisphere summer) when AC1+AC2
(163,532 kWh/month = 29% of site) runs at peak capacity. The PFC system is
correctly compensated for base load but **undersized for full summer AC load**.

**Annual kVA saving potential if corrected to PF 0.99:** ~R80,000/year (Switch 1)
**Annualised site-level saving:** ~R40,000–R77,000/year depending on correction quality.

### Main Switch 2 (PFC-B) — Reference System
No months below PF 0.95 in 24-month observation period.  
Annual saving potential to PF 0.99: only R4,802 — this system is correctly maintained.
**Use Switch 2 as the benchmark for what good PFC looks like.**

---

## High-Demand Threshold
Monitor PF specifically when demand > 85% of the site's historical peak:
- Site peak observed: 1,234 kVA → **85% threshold = 1,049 kVA**
- Switch 1 peak observed: 775 kVA → **85% threshold = 659 kVA**
- When demand is high AND PF is low, the kVA impact (and kVA demand charge) is greatest

---

## Agent Thresholds for PF Alerts

| Condition | Severity | Trigger |
|---|---|---|
| Switch-level PF < 0.90 | P1 CRITICAL | Immediate action |
| Switch-level PF < 0.95 | P2 WARNING | Schedule inspection |
| Switch-level PF 0.95–0.97 AND demand > 85% of peak | P2 WARNING | High-demand + marginal PF |
| Switch-level PF 0.95–0.97 | P3 WATCH | Monitor next month |
| Site-level only (PF 8323) | No alert | Site-level is not diagnostic |

---

## Recommended Remediation Process

> **IMPORTANT: The agent should NEVER estimate capacitor bank or PFC upgrade costs.**
> South African market pricing is highly variable and requires a site-specific assessment.

**Standard recommendation when PF < 0.95 is detected:**

1. **Step 1 — Augos PFC Assessment** (<R5,000 per system)  
   Contact Augos to arrange a Power Factor Correction assessment for the affected
   switch (Main Switch 1 in this case). The assessment will:
   - Identify root cause (failed capacitor stages, undersized for load, controller fault)
   - Quantify the improvement achievable
   - Provide accurate pricing for the specific remedy required
   - Typical turnaround: 1–2 weeks

2. **Step 2 — Implement remedy** (priced per assessment findings)  
   Options range from replacing faulty capacitor stages to adding capacity or
   upgrading to an automatic PFC controller — the assessment determines which applies.

3. **Step 3 — Verify via Augos data**  
   Monitor PF at switch level for 2–3 months post-remediation to confirm improvement.

**Do not quote installation costs in reports.** The assessment cost (<R5K) is the
correct first action and will produce accurate pricing.

---

## What NOT to Do

- ❌ Use site-level (8323) PF as the diagnostic metric
- ❌ Report "healthy PF" based on site-level average — Switch 1 may be below threshold
- ❌ Quote remediation capex from international benchmarks
- ❌ Raise a P1 alert for PF = 0.00 (this is a data parsing failure, not a real reading)
- ❌ Compare Switch 1 and Switch 2 loaded demand directly — they supply different loads

---

## Seasonal Calendar (Cape Town — Southern Hemisphere)

| Season | Months | AC Load | Expected PF on Switch 1 |
|---|---|---|---|
| Summer (peak) | Nov–Mar | High | ⚠️ Potentially < 0.95 |
| Autumn | Apr–May | Medium | Typically 0.97–0.99 |
| Winter | Jun–Aug | Low | 0.98–0.99 |
| Spring | Sep–Oct | Medium | Typically 0.97–0.99 |

AC1+AC2 is the primary inductive load driving PF degradation on Switch 1 in summer.
