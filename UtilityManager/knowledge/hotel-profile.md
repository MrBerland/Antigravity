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

## Cape Town Electricity Grid Context
- Eskom supplies the national grid; CoCT distributes locally
- Load shedding (Eskom rotational power cuts) was a significant issue 2022–2024 — hotel likely has backup generation
- Grid emission factor: **0.93 kgCO₂e/kWh** (Eskom NGER 2023/24)
- South Africa carbon tax: **ZAR 236/tonne CO₂e** (2025)
