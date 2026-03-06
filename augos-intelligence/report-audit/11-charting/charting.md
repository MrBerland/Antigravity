# Charting

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/charting?pointId=8323&productId=1` |
| **Purpose** | Custom, ad-hoc charting tool allowing users to select any measurement point and visualize any combination of parameters (Consumption, Peak Demand, Power Factor, etc.) over configurable time ranges. The most flexible visualization tool in the platform. |
| **Primary Users** | Energy Managers, Technical Analysts, Engineers |
| **Fuel Types** | All (Electricity, Water, Gas, Solar — parameter-dependent) |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Charting"
- **Action Buttons (right):** View Selection | Edit Parameters | Edit Date Range
- **Parameter Summary Bar:**
  - Measurement Point: One & Only|Cape Town (8323)
  - Parameters: Consumption, Peak Demand
  - Period: 2026/02/23 – 2026/02/23
  - Refresh icon (⟳)

### 2. AI Banner
- Purple gradient with "Download AI-Ready File (Beta)" CTA
- Same banner used across all reports

### 3. Chart Panels (★ Dynamic — One Per Parameter)

Each selected parameter generates its own independent chart panel. In this audit, 2 parameters were selected:

#### Panel 1: Consumption
- **Chart Type:** Bar chart (filled area/column)
- **Y-axis:** kWh
- **X-axis:** Time (Feb 23 12:00 → Feb 23 05:00, half-hourly)
- **Color:** Blue (#4169E1)
- **Data:** Half-hourly consumption values ranging ~200-400 kWh
- **Legend:** "● Consumption" at bottom center
- **Controls (top-right):**
  - Time resolution tabs: **Min** | **Halfhour** (active) | **Day** | **Month**
  - ✏️ Edit icon — modify chart parameters
  - 🗑️ Delete icon — remove this chart panel

#### Panel 2: Peak Demand
- **Chart Type:** Line chart
- **Y-axis:** kVA
- **X-axis:** Time (Feb 23 12:00 → Feb 23 05:00, half-hourly)
- **Color:** Blue line
- **Data:** Demand values ranging ~500-1200 kVA, showing clear business-hours peak
- **Legend:** "— Peak Demand" at bottom center
- **Controls:** Same as Panel 1 (Min | Halfhour | Day | Month + Edit + Delete)

### 4. Footer Summary Bar
- Repeats: Measurement Point | Parameters | Period
- ✏️ Edit icon | 🗑️ Delete icon for the entire chart configuration

---

## Components

### Parameter Selection Modal (★ Unique Interface)
- **Type:** Multi-step configuration wizard
- **Step 1:** Search and select a Measurement Point (autocomplete search input)
- **Step 2:** Select Parameters from available list (checkbox selection)
- **Action:** "Go" button to generate charts
- **Triggered by:** "Edit Parameters" button or first visit

### Highcharts Chart Panels
- **Library:** Highcharts (confirmed via `highcharts-container` class in DOM)
- **Chart Size:** 1292 × 300px per panel
- **Interactive Features:**
  - Hover tooltips showing exact values at each data point
  - Zoom/pan via click-drag on chart area
  - Time resolution switching (Min/Halfhour/Day/Month) without page reload

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Measurement Point | Autocomplete search | All accessible measurement points | None (must be selected) |
| Parameters | Multi-select checkboxes | Consumption, Peak Demand, Power Factor, Voltage, etc. | None (must be selected) |
| Date Range | Date pickers (From/To) | Any valid range | Today |
| Chart Resolution | Tab toggle (per chart) | Min, Halfhour, Day, Month | Halfhour |
| View Selection | Button | Opens parameter summary | — |
| Edit Parameters | Button | Re-opens selection modal | — |
| Edit Date Range | Button | Opens date picker | — |

---

## Downloads & Exports

| Export | Format | Trigger | Content |
|--------|--------|---------|---------|
| AI-Ready File | JSON | Banner button | Full chart data for selected parameters |

**Note:** Unlike other reports, Charting does NOT have XLSX/CSV/Copy exports. The AI file is the only export option.

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| User-configurable parameters | ✅ Choose any combination | ❌ Fixed parameters per report |
| Multi-panel layout (one chart per metric) | ✅ Stacked vertically | ❌ Pre-defined chart layouts |
| Per-chart time resolution | ✅ Each chart independently configurable | ❌ Global resolution only |
| Measurement point search | ✅ Full autocomplete search across all points | ❌ Bound to URL pointId |
| Edit/Delete per chart panel | ✅ Can remove individual charts | ❌ Fixed layout |
| No tables at all | ✅ Pure visualization tool | ❌ All others have tables |
| Highcharts library | ✅ Uses Highcharts | ❌ Others use Recharts |
| No section banners | ✅ Clean chart-only interface | ❌ Blue section headers |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **Flexible ad-hoc analysis** — Unlike fixed reports, users can combine any parameters they need.
2. **Cross-point comparison** — Can switch measurement points without leaving the page.
3. **Multi-resolution exploration** — Minute, half-hour, daily, and monthly views available per chart.
4. **Pattern discovery** — Overlaying consumption and demand reveals when peak demand occurs relative to usage.
5. **Quick drill-down** — Time resolution tabs allow zooming from monthly trend to minute-level detail instantly.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-consumption-bar-chart.png` | Header, parameter summary, AI banner, full Consumption bar chart (kWh, half-hourly) with Min/Halfhour/Day/Month tabs |
| 02 | `02-peak-demand-line-chart.png` | Bottom of Consumption chart, full Peak Demand line chart (kVA, half-hourly), footer summary bar |
| 03 | `03-full-page-bottom.png` | Same as 02 — confirms end of page content |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Parameters: Consumption, Peak Demand*
*Period: 23 February 2026 (default: today)*
