# Load Curtailment

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/load-curtailment?pointId=8323&productId=1` |
| **Purpose** | Monitor load shedding compliance and performance, tracking actual load vs curtailment targets, site/node compliance status, CBL (Curtailment Base Load) calculations, and energy trading capacity. Unique among all reports for its real-time operational focus. |
| **Primary Users** | Energy Managers, Operations, Grid Compliance Officers |
| **Fuel Types** | Electricity only |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Load Curtailment — One & Only|Cape Town (8323)"
- **Date range:** From 2026/02/23 00:00 / To 2026/02/23 23:59
- **Note:** Defaults to **today** (current day), unlike other reports which default to a month

### 2. AI Banner
- Purple gradient with "Download AI-Ready File (Beta)" CTA

### 3. Status Header (★ Unique)
- **Left panel:** "Stage 0 (No load shedding)" — displayed in amber/yellow text
- **Right panel:** "There is no data yet" — amber text indicating no active curtailment events

### 4. KPI Cards Row (4 cards)

| Card | Label | Value | Sub-metrics | Icon |
|------|-------|-------|-------------|------|
| 1 | **Current Trajectory** | 0 kW | 0.0% (green arrow), 0 A (orange arrow) | — |
| 2 | **Over Achieved (kWh)** | 0 | Node: 0 kWh (green up arrow) | — |
| 3 | **Site Compliant** | ✅ (green checkmark) | Over Achieved: 0 kWh, 0.0% | Progress bar (empty) |
| 4 | **Node Compliant** | ✅ (green checkmark) | Over Achieved: 0 kWh, 0.0% | Progress bar (empty) |

### 5. Dual Chart Section

**Left chart: Actual Load vs Curtailment Base Load (CBL)**
- **Date range:** 2026/02/23 00:00 to 2026/02/23 23:59
- **Type:** Line chart (currently empty — no load shedding data)
- **Y-axis:** kW
- **Time resolution tabs:** **1 min** | 30 min | Energy Worm
- **Legend:** Actual (kW) — orange | CBL (kW) — dark | Target (kW) — blue
- **Note:** Chart area is rendered but empty due to Stage 0

**Right chart: kWh Contribution to Target**
- **Date range:** 2026/02/23 00:00 to 2026/02/23 23:59
- **Y-axis:** kWh
- **Currently empty** — no target data

### 6. Performance Table (★ Most Complex — 6 Tabs)
- **Header:** Blue banner "Performance" with refresh icon, copy, XLSX, CSV exports, collapse toggle

**Tab navigation:**

| Tab | Purpose |
|-----|---------|
| **Site Performance** (active, green underline) | Time-series breakdown of actual vs target consumption |
| Node Performance | Aggregate node-level compliance data |
| Site CBL Calculation | How the Curtailment Base Load is calculated for this site |
| Site Contribution to Node Target | How this site contributes to the broader grid node target |
| Trade Capacity | Available energy trading capacity |
| Trading Dashboard | Energy trading activity and positions |

**Site Performance table columns:**

| Column Group | Columns |
|-------------|---------|
| **Consumption Schedule (kWh)** | Time, Actual, Target, Variance, Adj Target |
| **Cumulative Consumption (kWh)** | Actual, Target, Trades, Variance |
| **Available Energy** | kWh, % |

### 7. CBL Days Calendar (★ Unique — 12-Month Compliance View)
- **Header:** Blue banner "CBL Days"
- **Structure:** 12 individual month calendars in a 4×3 grid (March 2025 → February 2026)
- **Each month shows:** Mon–Sun columns, dates with status icons

**Calendar Legend:**

| Icon | Meaning | Color |
|------|---------|-------|
| ○ | CBL | White circle |
| ⊘ (red) | Load Shedding | Red strikethrough circle |
| ⊘ (green) | Abnormal Exclusion Days | Green strikethrough circle |
| ⊘ (amber) | Public Holiday | Amber strikethrough circle |

**Notable marked dates observed:**
- April 2025: 21st (🔴), 28th (🔴)
- May 2025: 18th (🔴)
- June 2025: 1st (🟢), 21st (🔴), 27th (🔴)
- August 2025: 9th (🔴)
- September 2025: 24th (🟢)
- October 2025: 15th (🔴)
- December 2025: 16th (🟢), 25th (🔴), 26th (🔴)
- January 2026: 1st (🔴)
- February 2026: 23rd (🔵 — today, highlighted in blue)

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Date From/To | DateTime pickers | Manual entry | Today (current day) |
| Chart resolution | Tab buttons | 1 min, 30 min, Energy Worm | 1 min |
| Performance tabs | Tab navigation | Site Performance, Node Performance, Site CBL Calculation, Site Contribution to Node Target, Trade Capacity, Trading Dashboard | Site Performance |
| Refresh | Icon button | Manual data refresh | — |

---

## Downloads & Exports

| Export | Format | Trigger | Content |
|--------|--------|---------|---------|
| AI-Ready File | JSON | Banner button | Full curtailment data |
| Download | Button | Top-level | Full report download |
| XLSX | Excel | Performance section icon | Performance table data |
| CSV | CSV | Performance section icon | Same in CSV |
| Copy | Clipboard | Performance section icon | Table data |

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| Real-time operational focus (defaults to today) | ✅ | ❌ (others default to month/year) |
| Load shedding stage indicator | ✅ Stage 0–8 | ❌ |
| Compliance status (Site + Node) | ✅ Dual compliance KPIs | ❌ |
| 6-tab performance section | ✅ Most tabs of any report | Max 4 tabs elsewhere |
| 12-month compliance calendar | ✅ Full year visual overview | ❌ |
| Trading dashboard integration | ✅ Energy trading data | ❌ |
| 1-minute resolution data | ✅ Ultra-granular | 30-min or daily elsewhere |
| CBL calculation transparency | ✅ Shows how base load is computed | ❌ |
| Trajectory indicator | ✅ Live kW with trend arrow | ❌ |
| Energy Worm chart view | ✅ Unique visualization | ❌ |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **Are we compliant?** — Dual compliance check: Site Compliant ✅ and Node Compliant ✅ with green checkmarks and progress bars.
2. **What stage is load shedding?** — "Stage 0 (No load shedding)" — real-time Eskom grid status.
3. **How much did we curtail vs target?** — Actual Load vs CBL chart shows the gap between what we used and what we should have used.
4. **What's our curtailment base load?** — Site CBL Calculation tab reveals the methodology.
5. **Can we trade energy?** — Trade Capacity and Trading Dashboard tabs show available capacity for demand response programs.
6. **What happened on specific days?** — 12-month calendar shows every load shedding event, public holiday, and abnormal exclusion day.
7. **How granular is the data?** — Down to 1-minute intervals for real-time operational decisions.

---

## Data States

### Current State (Stage 0)
- All KPIs show 0 values
- Charts render but are empty
- "There is no data yet" message displayed
- Calendar shows historical events only

### During Active Load Shedding (Expected)
- Stage indicator changes (1–8)
- Current Trajectory shows live kW reading
- Charts populate with real-time actual vs target lines
- Compliance status may change to ❌ if over target
- Over Achieved metric shows energy saved

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-kpi-cards-and-chart-header.png` | Stage 0 status, 4 KPI cards (Trajectory, Over Achieved, Site/Node Compliant), chart headers with 1min/30min/Energy Worm tabs |
| 02 | `02-chart-performance-tabs.png` | Empty chart area with legend (Actual/CBL/Target), Performance section with 6 tabs, Site Performance table headers |
| 03 | `03-compliance-calendar-mar-oct.png` | CBL Days calendar March–October 2025, marked load shedding events (red), exclusion days (green), with legend |
| 04 | `04-compliance-calendar-nov-feb.png` | CBL Days calendar November 2025–February 2026, December holidays marked, today (Feb 23) highlighted in blue |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Date range: 23 February 2026 (default: today)*
*Load shedding status: Stage 0 (No load shedding)*
