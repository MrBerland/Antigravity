# Tariff Context — One & Only Cape Town
## City of Cape Town: Large Power User (Medium Voltage) TOU

---

## Current Tariff Scheme
- **Authority:** City of Cape Town (CoCT) — Municipal Electricity
- **Scheme:** Large Power User (Medium Voltage) — Time of Use (TOU)
- **Currency:** ZAR (South African Rand)
- **Augos Tariff Scheme ID:** 11191 (confirmed from API data)
- **Augos Utility ID:** 5029

---

## Time-of-Use Periods (Typical CoCT MV TOU)

**Weekdays (Monday–Friday):**
| Period | Hours | Relative Rate |
|--------|-------|---------------|
| Peak | 07:00–10:00 and 18:00–20:00 | ~3× Off-Peak |
| Standard | 06:00–07:00, 10:00–18:00, 20:00–22:00 | ~2× Off-Peak |
| Off-Peak | 22:00–06:00 | Base rate |

**Weekends & Public Holidays:**
- Standard and Off-Peak periods only (no Peak periods)

**Note:** Exact period definitions and rates change annually with CoCT tariff review (typically July each year). Always verify current rates via the Augos tariff-comparison endpoint.

---

## Tariff Line Items (From Augos API)
Based on verified API data (January 2026, Point 8323):

| Tariff Type | ID | Unit | Example Rate (ZAR) |
|-------------|-----|------|-------------------|
| Consumption - standard | 56 | /kWh | R2.1708 |
| Consumption - standard (feed in) | 11 | /kWh | R1.1517 |
| Consumption - peak | 36 | /kWh | R3.3396 |
| Consumption - off-peak | 37 | /kWh | R1.7563 |

---

## Power Factor Penalties
The CoCT MV TOU tariff includes reactive power (kVAr) charges:
- **PF ≥ 0.95:** No penalty
- **PF 0.90–0.95:** Penalty charges apply
- **PF < 0.90:** Significant penalty — immediate capacitor bank review required

**Agent Action:** Alert Chief Engineer via P2 when PF < 0.92 (early warning).
Escalate to P1 when PF < 0.90.

---

## Demand Charges
- CoCT charges for Maximum Demand (kVA) — the highest 30-minute integrated demand in the billing period
- Exceeding the contracted demand triggers excess demand charges
- **Agent Action:** Monitor real-time demand vs contracted maximum. Alert at 95% of limit.

---

## Key Optimisation Opportunities
1. **ToU Shift:** Move shiftable loads (laundry, pool plant, EV charging) to Off-Peak (22:00–06:00)
2. **Peak Shaving:** Avoid running large loads simultaneously during Peak windows (07:00–10:00, 18:00–20:00)
3. **Power Factor Correction:** Maintain PF ≥ 0.95 via capacitor banks
4. **Demand Management:** Stagger HVAC startup to prevent demand spikes at 07:00
5. **Tariff Comparison:** Periodically check if alternative tariff schemes offer lower blended rates

---

## Solar / Feed-In
The API shows a "Consumption - standard (feed in)" tariff type (ID 11, R1.1517/kWh), suggesting the property may have or is eligible for solar PV feed-in. If solar is installed, the agent should:
- Track generation separately
- Calculate self-consumption ratio
- Report feed-in credits on financial reports
