# Technical Analysis

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/technical-analysis?pointId=8323&productId=1` |
| **Purpose** | Deep technical inspection of all measurement points. Real-time monitoring of demand, power, consumption, and power factor with granular statistics and historical context. |
| **Primary Users** | Energy Managers, Electrical Engineers, Maintenance Teams |
| **Fuel Types** | Electricity, Water, Fuel, Gas |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Technical Analysis — One & Only|Cape Town (8323)"
- **Navigation arrows:** `<` `>` to switch between sites

### 2. Fuel Selector
- Toggle buttons: **Electricity** (default), Water, Fuel, Gas

### 3. Date Range Controls
- **Preset buttons:** Today | Yesterday | Last 7 days | Last 30 days | Feb 26 | More
- **Manual pickers:** From/To datetime inputs
- **Note:** Date presets differ from Dashboard (includes "Last 7 days" and "Last 30 days" instead of "Two days ago" / "One week ago" / "Two weeks ago")

### 4. AI Banner
- Same as Dashboard — purple gradient with "Download AI-Ready File (Beta)" CTA

### 5. Technical Analysis Table
- **Header:** Blue banner "Technical Analysis" with refresh (↻), kebab menu (⋮), and collapse toggle (^)
- **Columns:**

| Column | Description | Example |
|--------|-------------|---------|
| Status Icon | Colored indicator (orange/yellow) showing data flow health | ● |
| Measurement Point | Name with serial number and Point ID | Cape Town (8323) |
| Last Activity | Most recent data timestamp | 2026/02/23 07:27 |
| Consumption | Total kWh for selected period | 5 047 kWh |
| Demand | Peak kVA reading | 803.3 kVA |
| PF | Power Factor | 0.99 |
| 📊 | "Show Statistics" chart icon | — |
| ⋮ | Per-row action menu | — |

### 6. Demand/Power Chart (Inline, per meter)
- **Type:** Highcharts time-series line chart
- **Located:** Below the selected meter row when expanded
- **Toggle tabs:** Demand/Power | Consumption | Power Factor
- **Y-axis:** kW/kVA (range 300–800 for site-level)
- **X-axis:** Time intervals at 30-min granularity
- **Series:** Two lines — Demand (red/pink) and Power (blue/purple)
- **Historical range slider:** Bottom sub-chart showing full data history (~May 2024 → Feb 2026)
- **Legend:** Demand — Power

### 7. "Show Statistics" Toggle
- **Collapsed by default** — Click to expand the Statistics table
- **Location:** Below the chart, above the meter list

### 8. Statistics Table (Expandable)
Granular technical metrics table with the following structure:

| Description | Usage | Maximum | Max Datestamp | Minimum | Min Datestamp |
|-------------|-------|---------|---------------|---------|---------------|
| Consumption (Total) (kWh) | 5 047 | — | — | — | — |
| Demand (Total) (kVA) | — | 803.3 | 2026/02/23 07:00 | 588.5 | 2026/02/23 03:00 |
| Power at peak (Total) (kW) | — | 792.5 | 2026/02/23 07:00 | — | — |
| Power factor at peak (Total) | — | 0.99 | 2026/02/23 07:00 | — | — |
| Reactive power at peak (Total) (kVar) | — | 131.3 | 2026/02/23 07:00 | — | — |
| Reactive energy (Total) (kVarh) | 865.6 | — | — | — | — |
| Demand A (Red) (kVA) | — | 295.9 | 2026/02/23 07:00 | 214.6 | 2026/02/23 03:00 |
| Demand B (White) (kVA) | — | *TBC* | — | — | — |
| Demand C (Blue) (kVA) | — | *TBC* | — | — | — |

**Key insight:** This table provides per-phase demand data (A/B/C), which is critical for identifying phase imbalance.

### 9. Meter Hierarchy List
Same expandable list as Dashboard, showing all measurement points:

**Main Switch 1 (PM46220418) (8324)** — 2 769 kWh, 413.0 kVA, PF 0.98
- AC1 and AC2 (8325) — 1 352 kWh, 262.4 kVA, PF 0.77
- Extractor fan1 (8327) — 125.4 kWh, 22.59 kVA, PF 0.76
- Heat pump hot water (8328) — 104.4 kWh, 17.38 kVA, PF 0.90
- Nobu (8329) — 76.91 kWh, 13.67 kVA, PF 0.91
- Penthouse 1 (8330) — 50.55 kWh, 7.14 kVA, PF -1.00
- Penthouse 2 (8331) — 27.11 kWh, 3.81 kVA, PF 0.97
- Penthouse 3 (8332) — 9.21 kWh, 1.71 kVA, PF -1.00
- Room 216 (8334) — 0 kWh

**Main Switch 2 (PM40510716) (8336)** — 2 202 kWh, 399.8 kVA, PF 0.99
- Boiler (8337) — 377.6 kWh, 153.2 kVA, PF 1.00
- Reubens (8338) — 284.1 kWh, 52.01 kVA, PF 1.00
- Spa (8339) — 234.1 kWh, 68.06 kVA, PF 1.00
- Villa/Pool (8341) — 404.8 kWh, 68.97 kVA, PF 0.86

---

## Differences from Dashboard

| Aspect | Dashboard | Technical Analysis |
|--------|-----------|-------------------|
| Summary cards | ✅ 4 cards with mini charts | ❌ Not present |
| Consumption Heatmap | ✅ Calendar view | ❌ Not present |
| Statistics Table | ❌ Not present | ✅ Granular tech stats |
| Per-phase demand | ❌ | ✅ A/B/C phase breakdown |
| Refresh button | ❌ | ✅ On table header |
| Chart default | Embedded in table | Same — inline per meter |
| Date presets | Today, Yesterday, 2d, 1w, 2w | Today, Yesterday, 7d, 30d, Month |

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Fuel Type | Toggle buttons | Electricity, Water, Fuel, Gas | Electricity |
| Date Range | Preset buttons | Today, Yesterday, Last 7 days, Last 30 days, [Month], More | Today |
| Date From/To | DateTime pickers | Manual entry | Current day 00:00–23:59 |
| Chart View | Tabs (per meter) | Demand/Power, Consumption, Power Factor | Demand/Power |
| Statistics | Toggle | Show/Hide statistics table | Hidden |

---

## Downloads & Exports

| Export | Format | Trigger |
|--------|--------|---------|
| AI-Ready File | JSON | Banner button "Download AI-Ready File (Beta)" |
| Kebab Menu | TBD | Table header kebab menu (⋮) — needs exploration |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **Operational health** — Is every meter reporting data? Check "Last Activity" for staleness.
2. **Peak demand identification** — Statistics table shows exact timestamp and value of maximum demand — critical for demand charge management.
3. **Power factor compliance** — PF values below 0.90 incur penalties; values of -1.00 indicate measurement issues.
4. **Phase imbalance detection** — Per-phase demand (A/B/C) reveals unbalanced loads that cause equipment stress.
5. **Reactive power audit** — Reactive energy (kVarh) totals help evaluate capacitor bank requirements.
6. **Historical trend** — Chart range slider goes back ~2 years, enabling long-term trend analysis.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-full-page-top.png` | Header, fuel tabs, AI banner, TA table with Cape Town row, Demand/Power chart |
| 02 | `02-demand-chart-and-meter-list.png` | Chart bottom with range slider, Show Statistics toggle, Main Switch 1 sub-meters |
| 03 | `03-meter-list-continued.png` | Remaining sub-meters |
| 04 | `04-statistics-table-expanded.png` | Full expanded Statistics table — Consumption, Demand, Power, PF, Reactive, per-phase |
| 05 | `05-show-statistics-toggle.png` | Show Statistics toggled open |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Date range: Today (2026/02/23)*
