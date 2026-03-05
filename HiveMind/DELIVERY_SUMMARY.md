# Augos Energy Data Extraction Summary
**Target Site:** Tiger Brands | Grains | Albany Bakeries | Bellville
**Point ID:** 10267 (Reporting Root)
**Generated:** 2026-02-01

## 1. Asset Registry
We have identified **10 Linked Measurement Points**, including:
- **Incomer 1**: `PM29521215` (Billing Point)
- **Incomer 2**: `PM44210717` (Billing Point)
- **Genset 1**: `PM59580323` (Supply)
- **Genset 2**: `PM59590323` (Supply)
- **Silos**: `PM57591022`
- **Workshop DB**: `PM67111024`
- **Admin DB**: `PM67101024`

These points are fully mapped in the system with their hierarchical relationships.

## 2. Financial Verification
We have successfully extracted billing data (via Xero Invoices), specifically **Invoice #INV-86432**.
- **Total Billed:** R3,680.00 (incl Tax) from "FTT"
- **Monitoring Fees:** R2,700.00 (Covering Incomers, Gensets, Admin/Workshop DBs)
- **Curtailment Fees:** R500.00 (Load Shedding Curtailment)
- **Usage Charges:** R0.00 (No kWh charges on this invoice)

## 3. Telemetry Gap Analysis
**CRITICAL FINDING:**
Despite checking both the core data warehouse (`pfc_daily_peaks`) and simulating the API requests (`/api/v1/power-factor-demand`) for the last 12 months for Point IDs **10267** and **37431729**, we found:
- **0 Daily Peak Records**
- **0 Consumption Records**

**Impact on Report:**
- **Load Profile (12m):** Cannot be generated (Missing Data)
- **Power Factor Report:** Cannot be generated (Missing Data)
- **Consumption Breakdown:** Cannot be generated (Missing Data)

## 4. Next Steps
You can run the attached `energy_report_final_v2.json` through Gemini. It contains all the above data structure. 
Gemini will be able to:
1.  **Draft the "Bill Verification" section** using the invoice data.
2.  **Highlight the "Missing Telemetry"** as a key insight/action item for the facility manager (e.g., "Check meter communications for Serial PM29521215...").
3.  **Validate the Asset List** against expected site equipment.

The JSON file is located at:
`/Users/timstevens/Antigravity/HiveMind/energy_report_final_v2.json`
