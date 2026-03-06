# Consumption Breakdown

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/consumption-breakdown?pointId=8323&productId=1` |
| **Purpose** | Visual and tabular breakdown of energy consumption across the full meter hierarchy. Shows where energy is being used, how much, and what percentage of total. |
| **Primary Users** | Energy Managers, Facility Managers, Sustainability Leads |
| **Fuel Types** | Electricity, Water, Fuel, Gas |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Consumption Breakdown — One & Only|Cape Town (8323)"

### 2. Fuel Selector
- Toggle buttons: **Electricity** (default), Water, Fuel, Gas

### 3. Date Range Controls
- **Preset buttons:** Last 7 days | Feb 26 | Jan 26 | Dec 25 | Nov 25 | More
- **Manual pickers:** From/To datetime inputs
- **Note:** Defaults to "Last 7 days" (unlike Dashboard/TA which default to "Today")

### 4. AI Banner
- Purple gradient with "Download AI-Ready File (Beta)" CTA

### 5. Consumption Breakdown Tree (★ Distinctive Component)
- **Type:** Interactive hierarchical tree diagram (SVG)
- **Structure:** Root → Main Switches → Sub-meters
- **Data shown per node:**
  - 🟠 kWh value (absolute consumption)
  - 🔵 Percentage of parent (relative contribution)
- **Color coding:** Each branch has a distinct color bar (green, gold, pink, blue, etc.)
- **"Not measured" labels:** Appear in red where the sum of children doesn't match the parent — indicating unmetered consumption

**Tree data (Last 7 days):**
```
Cape Town (8323) — 137,517 kWh (100.00%)
├── Main Switch 1 (8324) — 77,127 kWh (56.09%)
│   ├── AC1 and AC2 (8325) — 40,438 kWh
│   ├── Extractor fan1 (8327) — 2,945 kWh
│   ├── Heat pump hot water (8328) — 2,175 kWh
│   ├── Nobu (8329) — 3,874 kWh
│   ├── Penthouse 1 (8330) — 1,034 kWh
│   ├── Penthouse 2 (8331) — 732.9 kWh
│   ├── Penthouse 3 (8332) — 118.1 kWh
│   ├── Room 216 (8334) — 0.0 kWh
│   └── [Not measured] — 25,810 kWh (18.77%) ← RED
├── Main Switch 2 (8336) — 60,391 kWh (43.91%)
│   ├── Boiler (8337) — 12,823 kWh
│   ├── Reubens (8338) — 7,141 kWh
│   ├── Spa (8339) — 6,069 kWh
│   ├── Villa/Pool (8341) — 11,650 kWh
│   └── [Not measured] — 22,709 kWh (16.51%) ← RED
```

### 6. Horizontal Scroll Bar
- Below the tree — allows panning when the tree is wider than viewport

### 7. Total Consumption Charts (Side by Side)

#### 7a. Stacked Bar Chart (Left — ~70% width)
- **Type:** Highcharts stacked bar/area chart
- **Y-axis:** kWh (0–600 range)
- **X-axis:** Date/time (Feb 16–Feb 23 at "Half-hour" granularity)
- **Series:** Main Switch 1 (8324) in gold/khaki, Main Switch 2 (8336) in pink
- **Toggle:** Halfhour | Day granularity switch
- **Legend:** Main Switch 1 (8324) — Main Switch 2 (8336)

#### 7b. Donut Chart (Right — ~30% width)
- **Type:** Donut/ring chart
- **Center value:** "137 517 Site Total"
- **Segments:** Main Switch 1 (gold) and Main Switch 2 (pink) proportional to consumption
- **Purpose:** Immediate visual split between the two main feeds

### 8. Consumption Log Table
- **Header:** Blue banner "Consumption Log" with copy (📋), XLSX, CSV export buttons and collapse toggle
- **Columns:**

| Column | Description | Example |
|--------|-------------|---------|
| Measurement Point | Full name with parent context | Main Switch 1|AC1 and AC2 (8325) |
| Serial No. | Meter serial number | PM50401119 |
| Start (kWh) | Meter reading at period start | 22,883,587 |
| End (kWh) | Meter reading at period end | 22,924,024 |
| Consumption (kWh) | Difference (End - Start) | 40,438 |

- **Row count:** 15 rows (site + all sub-meters)

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Fuel Type | Toggle buttons | Electricity, Water, Fuel, Gas | Electricity |
| Date Range | Preset buttons | Last 7 days, [Months], More | Last 7 days |
| Date From/To | DateTime pickers | Manual entry | Last 7 days range |
| Chart Granularity | Toggle | Halfhour, Day | Halfhour |

---

## Downloads & Exports

| Export | Format | Trigger | Content |
|--------|--------|---------|---------|
| AI-Ready File | JSON | Banner button | Structured consumption data |
| XLSX | Excel | "Consumption Log" XLSX icon | Meter start/end/consumption readings |
| CSV | CSV | "Consumption Log" CSV icon | Same as XLSX in comma-delimited format |
| Copy | Clipboard | "Consumption Log" copy icon (📋) | Table data to clipboard |

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| Hierarchy Tree Diagram | ✅ Full visual tree | ❌ |
| "Not measured" detection | ✅ Red labels showing unmetered consumption | ❌ |
| Donut chart (site total) | ✅ | ❌ |
| Stacked bar with granularity toggle | ✅ Halfhour/Day | ❌ |
| Meter register readings (Start/End) | ✅ | ❌ (other reports show calculated values only) |
| XLSX/CSV direct export | ✅ On Consumption Log | Some reports have, some don't |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **Where is energy being consumed?** — Tree diagram immediately shows which areas consume the most.
2. **How much energy is unaccounted for?** — "Not measured" values reveal the gap between a main meter and its sub-meters. High percentages (18.77%, 16.51%) suggest unmeasured loads or potential leaks/theft.
3. **How is consumption distributed between main feeds?** — Donut chart shows Main Switch 1 (56%) vs Main Switch 2 (44%).
4. **What does the consumption profile look like over time?** — Stacked bar chart reveals daily patterns, weekend vs weekday differences, and unusual spikes.
5. **What are the actual meter register readings?** — Consumption Log shows raw Start/End readings, useful for verifying municipal billing.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-hierarchy-tree.png` | Full hierarchy tree showing Cape Town → Main Switches → Sub-meters with kWh and % values |
| 02 | `02-stacked-bar-and-donut-chart.png` | Total Consumption stacked bar chart (Halfhour) + donut chart (137,517 Site Total) + Consumption Log header |
| 03 | `03-consumption-log-table-top.png` | Consumption Log table with headers and first 12 rows showing meter readings |
| 04 | `04-consumption-log-table-full.png` | Full Consumption Log table showing all 15 meter rows |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Date range: Last 7 days (2026/02/16 – 2026/02/23)*
