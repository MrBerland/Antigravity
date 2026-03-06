# Dashboard

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/dashboard?pointId=8323&productId=1` |
| **Purpose** | High-level operational overview of all measurement points at a site. Quick health check for consumption, demand, power factor, and data recency. |
| **Primary Users** | Facility Managers, Energy Managers, Operations Teams |
| **Fuel Types** | Electricity, Water, Fuel, Gas |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Site Title:** "Dashboard — One & Only|Cape Town (8323)"
- **Navigation arrows:** `<` `>` to switch between sites
- **Close button:** `×` to deselect site

### 2. Fuel Selector
- Toggle buttons: **Electricity** (default active), Water, Fuel, Gas
- Switching fuel type reloads all data on the page

### 3. Date Range Controls
- **Preset buttons:** Today | Yesterday | Two days ago | One week ago | Two weeks ago | More
- **Manual pickers:** From `2026/02/23 00:00` / To `2026/02/23 23:59`
- **Kebab menu** (⋮): Additional date options

### 4. AI Banner
- Purple gradient banner across full width
- Text: *"New! Unlock your data's potential with AI. Download raw Augos report data to provision your AI tools."*
- **CTA button:** "Download AI-Ready File (Beta)"
- Triggers JSON download of structured report data

### 5. Summary Cards (4 cards in a row)
- **Position:** Directly below AI banner
- **Content:** Key metrics for the selected period (appear to show consumption overview charts/stats)
- **Note:** Cards contain stacked bar charts showing hourly consumption breakdown
- *Requires further investigation on specific metrics displayed*

### 6. Consumption Heatmap Calendar (right side, adjacent to cards)
- **Type:** Calendar bubble chart
- **Layout:** Days of week (Mon–Sun) × Week numbers (W32–W9, ~6 months)
- **Color scale:** Green (low) → Yellow (medium) → Orange (high) → Red (very high)
- **Toggles:** Consumption | Demand/Power | Power Factor
- **Each bubble:** Shows the day-of-month number, color-coded by intensity

### 7. Technical Analysis Table
- **Header:** Blue banner "Technical Analysis" with kebab menu (⋮) and collapse toggle (^)
- **Columns:**

| Column | Description | Example |
|--------|-------------|---------|
| Measurement Point | Name, serial number, and Point ID | Cape Town (8323) |
| Last Activity | Most recent data timestamp | 2026/02/23 07:21 |
| Consumption | Total kWh for selected period | 4 889 kWh |
| Demand | Peak kVA reading | 805.8 kVA |
| PF | Power Factor (0–1.00) | 0.99 |
| 📊 | "Show Statistics" — opens inline chart | — |
| ⋮ | Action menu for the point | — |

- **Row behavior:** Each row is expandable (concertina) to show child/sub-meters
- **Status indicators:** Colored chevron (yellow = active, indicating data flow status)

### 8. Site Meter Hierarchy (expanded from table)
Full list of all measurement points under this site:

**Main Switch 1 (8324)** — Sub-meters:
| Point | ID | Consumption | Demand | PF |
|-------|----|-------------|--------|-----|
| AC1 and AC2 | 8325 | 1 037 kWh | 248.8 kVA | 0.78 |
| Extractor fan1 | 8327 | 122.1 kWh | 22.59 kVA | 0.76 |
| Heat pump hot water | 8328 | 101.4 kWh | 17.38 kVA | 0.90 |
| Nobu | 8329 | 74.98 kWh | 13.67 kVA | 0.91 |
| Penthouse 1 | 8330 | 49.29 kWh | 7.14 kVA | -1.00 |
| Penthouse 2 | 8331 | 26.40 kWh | 3.81 kVA | 0.97 |
| Penthouse 3 | 8332 | 9.00 kWh | 2.06 kVA | 1.00 |
| Room 216 | 8334 | 0 kWh | — | — |

**Main Switch 2 (8336)** — Sub-meters:
| Point | ID | Consumption | Demand | PF |
|-------|----|-------------|--------|-----|
| Boiler | 8337 | 377.6 kWh | 153.2 kVA | 1.00 |
| Reubens | 8338 | 284.1 kWh | 52.01 kVA | 1.00 |
| Spa | 8339 | 234.1 kWh | 68.06 kVA | 1.00 |
| Villa/Pool | 8341 | 404.8 kWh | 68.97 kVA | 0.86 |

### 9. Inline Demand/Power Chart
- **Type:** Highcharts time-series line chart
- **Shown when:** "Show Statistics" icon is clicked on a meter row
- **Toggle tabs:** Demand/Power | Consumption | Power Factor
- **Y-axis:** kW/kVA (range ~300–800 for site level)
- **X-axis:** Time intervals (30-min granularity for "Today")
- **Series:** Two lines — Demand (blue) and Power (purple/pink)
- **Time slider:** Range selector at bottom for zooming into specific intervals
- **Legend:** Demand — Power
- **Historical range:** Slider shows data back to ~May 2024

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Fuel Type | Toggle buttons | Electricity, Water, Fuel, Gas | Electricity |
| Date Range | Preset buttons | Today, Yesterday, 2 days, 1 week, 2 weeks, More | Today |
| Date From/To | DateTime pickers | Manual entry | Current day 00:00–23:59 |
| Chart View | Tabs (per meter) | Demand/Power, Consumption, Power Factor | Demand/Power |
| Heatmap View | Tabs | Consumption, Demand/Power, Power Factor | Consumption |
| Statistics | Toggle per row | Show/Hide inline chart | Hidden |

---

## Downloads & Exports

| Export | Format | Trigger |
|--------|--------|---------|
| AI-Ready File | JSON | Banner button "Download AI-Ready File (Beta)" |
| Data Download | CSV/Excel | Available via Data Download report (separate page) |
| Chart Export | PNG/PDF | Via Highcharts context menu (if enabled) |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

Expected endpoints:
- `GET /api/points/{pointId}/hierarchy` — Meter tree structure
- `GET /api/points/{pointId}/dashboard-summary` — Summary card data
- `GET /api/points/{pointId}/consumption-heatmap` — Calendar data
- `GET /api/points/{pointId}/technical-analysis` — Table data
- `GET /api/points/{pointId}/statistics` — Chart time-series data

---

## Key Insights This Report Provides

1. **Is data flowing?** — Last Activity column shows data recency per meter. Stale timestamps indicate communication issues.
2. **Which meters are consuming the most?** — Quick comparison of kWh across all sub-meters.
3. **Are there demand spikes?** — Demand/Power chart shows peak events in real-time.
4. **What's the power factor?** — PF column flags low power factor (<0.9) that incurs utility penalties.
5. **Seasonal patterns** — Heatmap reveals weekly/monthly consumption patterns at a glance.
6. **Infrastructure overview** — Full meter hierarchy establishes the physical relationship between main switches and sub-meters.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-full-page-top.png` | Header, fuel tabs, date controls, AI banner, summary cards |
| 02 | `02-charts-and-technical-analysis.png` | Stacked bar charts, heatmap calendar, Technical Analysis table header with Cape Town row |
| 03 | `03-demand-chart-and-meter-list.png` | Demand/Power line chart with range slider, Show Statistics toggle, Main Switch 1 sub-meters |
| 04 | `04-meter-list-and-heatmap.png` | Main Switch 2 sub-meters, Consumption Heatmap calendar |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Date range: Today (2026/02/23)*
