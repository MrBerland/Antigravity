# Hotel Profile — One & Only Cape Town
**Point ID:** 8323 | **Environment:** live.augos.io | **Currency:** ZAR

## Property Overview
One & Only Cape Town is a flagship ultra-luxury resort operated by Kerzner International, located at the V&A Waterfront. It is one of the most prominent 5-star properties in Africa and serves as the sustainability benchmark hotel for this agent.

## Location & Climate
- **Address:** Dock Road, V&A Waterfront, Cape Town, 8001, South Africa
- **Coordinates:** -33.9249°S, 18.4241°E
- **Climate Zone:** Mediterranean (hot, dry summers; mild, wet winters)
- **Cape Town Summer (Dec–Feb):** 25–35°C, strong SE winds, peak AC demand
- **Cape Town Winter (Jun–Aug):** 8–18°C, rain, peak heating + hot water demand
- **Southeaster (Cape Doctor):** Strong SE wind in summer — affects cooling tower efficiency and HVAC loads significantly

## Utility Infrastructure
- **Electricity Supply:** City of Cape Town (CoCT) — Large Power User Medium Voltage TOU tariff
- **Tariff Scheme:** Time-of-Use (Peak / Standard / Off-Peak periods apply)
- **Metering:** Augos Nova meters across all major circuits
- **Water Source:** City of Cape Town municipal supply (post-Day Zero water restrictions still influence operational practices)
- **Gas:** Natural gas / LPG for kitchen and water heating

## Sustainability Framework
- **EarthCheck:** Mandatory certification across Kerzner portfolio since 2019
- **World Sustainable Hospitality Alliance:** Kerzner joined April 2025, committed to "Net Positive Hospitality"
- **Goal:** Give back more than the property consumes across people, planet, place, and prosperity

## Key Engineering Considerations
1. **Power Factor:** On CoCT MV TOU, PF penalties apply. Target PF ≥ 0.95 at all times.
2. **Demand Management:** Contracted demand limit — exceeding triggers significant excess charges on CoCT tariff.
3. **Time-of-Use Optimisation:** Peak window (typically 07:00–10:00 and 18:00–20:00 weekdays) attracts 3× off-peak rate.
4. **Water Security:** Cape Town's water scarcity history (Day Zero 2018) means water efficiency is a reputational and operational priority.
5. **Base Load Scrutiny:** Large hotels have significant always-on loads (refrigeration, BMS, HVAC standby). Rising base load = inefficiency creeping in.

## Typical Consumption Profile (Indicative)
- **Peak electricity demand:** Expected during summer afternoons (AC) and breakfast/dinner service
- **Peak water demand:** Check-in wave (~14:00) and morning ablution peak (~07:00–09:00)
- **Peak gas demand:** Breakfast service (06:00–10:00) and dinner service (17:00–22:00)
- **Overnight base loads:** Refrigeration, BMS, security, emergency lighting, boiler standby

- Eskom supplies the national grid; CoCT distributes locally
- Load shedding (Eskom rotational power cuts) was a significant issue 2022–2024 — hotel likely has backup generation
- Grid emission factor: **0.93 kgCO₂e/kWh** (Eskom NGER 2023/24)
- South Africa carbon tax: **ZAR 236/tonne CO₂e** (2025)

---

## Energy Sources — Confirmed Status (March 2026)

| Source | Status | Notes |
|---|---|---|
| Grid (CoCT MV TOU) | ✅ Active | Primary supply. 100% of recorded consumption is grid import |
| Solar PV | ❌ Not installed | Feed-in tariff line (tariffTypeID 11, R-0.01) is a CoCT billing template artifact — not actual generation |
| Generator | ❓ Unknown | Likely present given property size and load shedding history. Confirm with Chief Engineer |
| BESS | ❓ Unknown | Confirm with Chief Engineer |

**Implication for analysis:**
All consumption recorded in Augos is grid import. The EnPI model (kWh/CDD) is
accurate as-is — no generation offset required. The R-0.01 feed-in credit in
the billing data is noise and should be filtered in bill verification.

**Strategic note — Solar opportunity:**
Cape Town has one of the best solar resources in South Africa (~2,200 kWh/kWp/year).
At R2.483/kWh grid rate (rising ~12%/year), a solar PV installation would be
on a compelling payback. The feed-in tariff (R1.1517/kWh) is pre-configured in
the billing structure — CoCT is ready to accept generation if installed.
This is a Phase 3 what-if simulation candidate once the core system is established.

---

## Open Site Profile Items (Require Confirmation)

| Item | Why it matters | From whom |
|---|---|---|
| NMD (kVA) | Enables demand monitoring + potential NMD reduction saving | CoCT electricity supply agreement |
| Generator: installed, capacity, ATS | Load shedding diesel cost, Scope 1 carbon, maintenance calendar | Chief Engineer |
| BESS: installed, capacity | Demand management strategy | Chief Engineer |
| Transformer: capacity, last oil test, last thermal scan | Compliance calendar | Chief Engineer / Electrical records |
| PFC Switch 1: capacity, stages, last survey | PF remediation sizing | Chief Engineer / Augos |
| PFC Switch 2: capacity, stages, last survey | Confirmation this system is correctly sized | Chief Engineer / Augos |
| Certificate of Compliance: last issued, expiry | Legal compliance flag | Chief Engineer |
| Last thermographic scan date | Compliance calendar — recommended annual | Chief Engineer |

