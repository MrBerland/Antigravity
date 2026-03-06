# SM-01: Sensors (Dashboard)

> **Module:** Sensing & Monitoring  
> **URL:** `live.augos.io/app/sensing-and-monitoring/status`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Sensors Dashboard is the landing page for the Sensing & Monitoring module. It provides a real-time operational view of all connected measurement devices across a site, allowing operators to monitor device health, compliance, and instantaneous readings at a glance.

---

## Page Layout

### Header Bar
| Element | Description |
|---------|-------------|
| **Page Title** | "Sensors" with blue left-border accent |
| **Site Selector** | Autocomplete dropdown — selects the property/site to view |
| **View Tabs** | `Instantaneous` · `State` — toggles between two data modes |
| **Date Controls** | Quick-select buttons: `Feb 26` · `Jan 26` · `Dec 25` · `Nov 25` · `More` |
| **AI Export** | Purple gradient banner: "🚀 Unlock your data's potential with AI" + `Download AI-Ready File (Beta)` button |

### Instantaneous View
Shows real-time and historical readings for each sensor/measurement point.

| Column | Description |
|--------|-------------|
| **Description** | Sensor name and measurement point ID |
| **Last Reading** | Most recent value with unit (e.g., `45.2 kWh`) |
| **High** | Highest value in the selected period |
| **Low** | Lowest value in the selected period |
| **Last 50 Readings** | Inline sparkline chart showing trend |
| **Breach Count** | Number of threshold breaches |
| **Compliance %** | Percentage of time within acceptable range |

### State View
Shows binary/state-based sensors (machines, switches, contactors).

| Column | Description |
|--------|-------------|
| **Description** | Production line / equipment name |
| **Status** | `RUNNING` (green) or `NOT RUNNING` (red) badges |
| **Compliance Timeline** | Horizontal bar showing running/stopped periods across the day |
| **Breach Count** | Number of state violations |
| **Compliance %** | Uptime percentage |
| **Event Count** | Total state-change events in period |

### Detail View
Clicking a sensor row opens an expanded detail panel showing:
- Historical readings chart
- Breach event log
- Compliance summary statistics

---

## Functional Components

### 1. Site Selector
- **Type:** Autocomplete dropdown with search
- **Behavior:** Filters all sensor data to the selected site
- **Default:** Empty state (no site selected)
- **Observed Sites:** Cape Town, One & Only Cape Town, Isikhwama Manufacturing

### 2. View Toggles
- **Instantaneous:** For analog/numeric sensors (voltage, current, consumption)
- **State:** For binary/discrete sensors (machine on/off, contactors)

### 3. Temporal Controls
- Quick-select month buttons with "More" opening a dual-calendar date range picker
- The date range modal has tabs: `Date Range` and `Calendar Month`

### 4. Data Export
- AI-Ready File download (Beta) — structured JSON with `_aiInstructions` block
- Standard data table export capabilities

---

## Data Points Observed

| Site | Sensors (Instantaneous) | Sensors (State) |
|------|------------------------|-----------------|
| One & Only Cape Town | 0 | 0 |
| Cape Town | 0 | 0 |
| Isikhwama Manufacturing | Multiple | 12 production lines |

**State Sensor Examples (Isikhwama):**
- Production Line 1–12 with RUNNING/NOT RUNNING status
- Compliance timelines show green (running) and red (stopped) bands
- Event counts ranging from 2–15 per line per day

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| GET | `/api/sensing-monitoring/status` | `site_id`, `date_from`, `date_to`, `view_type` |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-state-view.png` | State view with 12 production lines at Isikhwama Manufacturing |
| `02-instantaneous-view.png` | Instantaneous view with High/Low values and sparklines |
| `03-date-range-modal.png` | Dual calendar date range picker modal |
| `04-empty-state.png` | Initial empty state before site selection |

---

## Key Insights

1. **Dual-mode dashboard** — Instantaneous for numeric sensors, State for binary sensors
2. **Compliance-first design** — Every sensor shows compliance % and breach count
3. **Sparkline integration** — Last 50 readings rendered inline for quick trend analysis
4. **Manufacturing focus** — State view clearly designed for production line monitoring
5. **Consistent UI patterns** — Same date controls, AI export, and site selector as Utilities & Services
