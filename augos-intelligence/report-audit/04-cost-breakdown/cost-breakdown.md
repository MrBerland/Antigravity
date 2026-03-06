# Cost Breakdown

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/cost-breakdown?pointId=8323&productId=1` |
| **Purpose** | Financial breakdown of electricity costs by tariff charge type, including consumption by TOU period, demand charges, and fixed charges. Includes 12-month trend sparklines and sub-meter cost attribution. |
| **Primary Users** | Finance Teams, Energy Managers, Procurement, C-Suite |
| **Fuel Types** | Electricity (primary — tariff-dependent) |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Cost Breakdown — One & Only|Cape Town (8323)"

### 2. Fuel Selector
- Toggle buttons: **Electricity** (default), Water, Fuel, Gas

### 3. Date Range Controls
- **Preset buttons:** Feb 26 | **Jan 26** (active) | Dec 25 | Nov 25 | Oct 25 | More
- **Manual pickers:** From 2026/01/01 00:00 / To 2026/01/31 23:59
- **Note:** Defaults to month-based selection (this is a monthly billing-oriented report)

### 4. AI Banner
- Purple gradient with "Download AI-Ready File (Beta)" CTA

### 5. Cost Distribution Bar (★ Distinctive Component)
- **Type:** Horizontal stacked percentage bar
- **Color-coded segments with legend:**
  - 🔵 Consumption - standard: **36.3%**
  - 🟢 Consumption - standard (feed in): **0%**
  - 🔴 Consumption - peak: **20.88%**
  - 🟢 Consumption - off-peak: **34.3%**
  - 🟤 Demand charge: **6.78%**
  - ⚫ Monthly service charge: **0.17%**
  - 🟣 Network access charge: **1.56%**

### 6. Cost Breakdown Table
- **Header:** Blue banner "Cost Breakdown" with tariff info, XLSX/CSV/Copy buttons, kebab menu, collapse toggle
- **Tariff displayed:** "City of Cape Town | Large Power User (Medium Voltage) TOU"
- **Tabs:** Fixed Charges Included | Fixed Charges Excluded
- **Columns:**

| Column | Description | Example |
|--------|-------------|---------|
| Color | Color swatch matching distribution bar | 🔵 |
| Item | Charge description | Consumption - standard |
| Units | Quantity | 231,071.56 |
| Unit | Unit of measure | kWh |
| Rate (ZAR) | Unit rate | 2.1708 |
| Total (ZAR) | Total cost | 501,610.16 |
| % of Total | Percentage of total bill | 36.3% |
| 12 Month Trend | Sparkline showing 12-month history | 📈 |

**Row data (Jan 2026):**

| Item | Units | Unit | Rate (ZAR) | Total (ZAR) | % |
|------|-------|------|------------|-------------|---|
| Consumption - standard | 231,071.56 | kWh | 2.1708 | 501,610.16 | 36.3% |
| Consumption - standard (feed in) | -0.01 | kWh | 1.1517 | -0.02 | 0% |
| Consumption - peak | 86,392.4 | kWh | 3.3396 | 288,516.06 | 20.88% |
| Consumption - off-peak | 269,877.47 | kWh | 1.7563 | 473,985.81 | 34.3% |
| Demand charge | 1,233.61 | kVA | 75.89 | 93,618.76 | 6.78% |
| Monthly service charge | 1 | Month | 2,404.57 | 2,404.57 | 0.17% |
| Network access charge | 1,233.53 | kVA | 17.47 | 21,549.79 | 1.56% |
| **Total** | | | | **1,381,685.13** | **99.99%** |

### 7. Sub Measurement Cost Breakdown
- **Header:** Blue banner "Sub Measurement Cost Breakdown" with copy button, collapse toggle
- **Columns:**

| Column | Description | Example |
|--------|-------------|---------|
| Measurement Point | Sub-meter name | Main Switch 1 (8324) |
| Consumption (kWh) | Total kWh for period | — |
| Demand (kVA) | Peak demand for period | — |
| Cost (ZAR) | Calculated estimated cost | — |
| 12 Month Trend | Sparkline | 📈 |

- **"Add measurement point"** button — opens selector to add sub-meters to this view
- **Note:** Sub-measurement costs are proportionally allocated from the site total

### 8. Trend Charts (3 stacked, full-width)

#### 8a. Cost (ZAR) Chart
- **Type:** Line chart (orange)
- **Y-axis:** ZAR (range 0–1M)
- **X-axis:** Days of month
- **Shows:** Daily cost fluctuations
- **Range slider:** Bottom sub-chart for historical context

#### 8b. Aggregate kWh Cost (ZAR) Chart
- **Type:** Line chart (blue/purple)
- **Y-axis:** ZAR (range 0–2)
- **X-axis:** Days of month
- **Shows:** Cost per kWh over time (blended rate)
- **Range slider:** Bottom sub-chart

#### 8c. Consumption (kWh) Chart
- **Type:** Line chart (orange)
- **Y-axis:** kWh (range 0–500k)
- **X-axis:** Days of month

#### 8d. Demand (kVA) Chart
- **Type:** Line chart (blue)
- **Y-axis:** kVA (range 0–1k)
- **X-axis:** Days of month
- **Range slider:** Bottom sub-chart

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Fuel Type | Toggle buttons | Electricity, Water, Fuel, Gas | Electricity |
| Date Range | Preset buttons | Monthly presets (Feb 26, Jan 26, Dec 25, etc.) | Current/Previous month |
| Date From/To | DateTime pickers | Manual entry | Month start–end |
| Fixed Charges | Tab toggle | Fixed Charges Included, Fixed Charges Excluded | Included |
| Sub Meters | Button | "Add measurement point" | — |

---

## Downloads & Exports

| Export | Format | Trigger | Content |
|--------|--------|---------|---------|
| AI-Ready File | JSON | Banner button | Complete cost data structure |
| XLSX | Excel | Cost Breakdown header XLSX icon | Cost table data |
| CSV | CSV | Cost Breakdown header CSV icon | Cost table data |
| Copy | Clipboard | Cost Breakdown header copy icon (📋) | Table data to clipboard |

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| Cost distribution bar | ✅ Color-coded percentage split | ❌ |
| TOU period breakdown | ✅ Standard/Peak/Off-peak rates | ❌ (except Time of Use report) |
| Tariff name displayed | ✅ "City of Cape Town \| Large Power User (Medium Voltage) TOU" | ❌ |
| 12-month sparklines | ✅ In every row | ❌ (only some reports) |
| Fixed charges toggle | ✅ | ❌ |
| Sub-meter cost allocation | ✅ | ❌ |
| 4 trend charts (Cost, Agg kWh, Consumption, Demand) | ✅ | Partial in others |
| Feed-in (negative consumption) | ✅ | ❌ |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **What is the total electricity bill?** — ZAR 1,381,685.13 for January 2026 (clear monthly total).
2. **What drives the bill?** — Distribution bar immediately shows 36.3% standard + 34.3% off-peak + 20.88% peak consumption.
3. **What is the tariff rate per charge?** — Rate column shows exact ZAR/kWh for each TOU period and ZAR/kVA for demand.
4. **Is the tariff right?** — Tariff name ("City of Cape Town | Large Power User (Medium Voltage) TOU") displayed prominently for verification.
5. **How do costs trend over time?** — 12-month sparklines in every row show if costs are increasing or decreasing.
6. **How much do sub-meters contribute?** — Sub Measurement section attributes costs to individual areas.
7. **Is there any feed-in/export?** — "Standard (feed in)" row shows if any energy is being exported back to the grid.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-distribution-bar-and-cost-table.png` | Distribution bar, tariff info, cost table with sparklines showing standard/peak/off-peak/demand rows |
| 02 | `02-totals-and-sub-measurement.png` | Monthly service & network charges, total (R1,381,685), sub-measurement table, "Add measurement point" |
| 03 | `03-cost-and-aggregate-charts.png` | Cost (ZAR) line chart, Aggregate kWh Cost (ZAR) chart, start of Consumption chart |
| 04 | `04-consumption-and-demand-charts.png` | Consumption (kWh) and Demand (kVA) line charts at bottom of page |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Date range: January 2026 (2026/01/01 – 2026/01/31)*
