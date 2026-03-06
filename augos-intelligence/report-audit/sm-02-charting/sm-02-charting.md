# SM-02: Charting

> **Module:** Sensing & Monitoring  
> **URL:** `live.augos.io/app/sensing-and-monitoring/charting`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Charting report provides interactive time-series visualization for any measurement point parameter. Users select a point, choose parameters (Consumption, Peak Demand, Power, Power Factor), set a date range, and render high-fidelity bar/line charts at configurable intervals.

---

## Page Layout

### Header Bar
| Element | Description |
|---------|-------------|
| **Page Title** | "Charting" with blue left-border accent |
| **View Selection** | Button to open/modify current chart selection |
| **Edit Parameters** | Button to change displayed parameters |
| **Edit Date Range** | Button to modify the time period |

### Selection Summary
- **Measurement Point:** Name + ID (e.g., "3 The Terrace (45829614)")
- **Parameters:** Selected parameter names (e.g., "Consumption")
- **Period:** Date range (e.g., "2026/02/01 - 2026/02/28")
- **Reload button** (↻) to refresh data

### AI Export Banner
Purple gradient banner with `Download AI-Ready File (Beta)` button

### Chart Area
| Element | Description |
|---------|-------------|
| **Chart Title** | Parameter name (e.g., "Consumption") |
| **Interval Toggle** | `Min` · `Halfhour` · `Day` · `Month` |
| **Y-Axis** | Value with unit label (e.g., "kWh") |
| **X-Axis** | Date/time labels at selected interval |
| **Chart Type** | Vertical bar chart (SVG rendered) |
| **Legend** | Color-coded parameter labels below chart |
| **Edit/Delete** | Pencil (✏) and trash (🗑) icons per chart |

### Multiple Charts
A second measurement point can be added — each renders as its own chart panel with independent interval controls.

---

## Functional Components

### 1. Selection Modal
- **Step 1:** Select Measurement Point (autocomplete dropdown with search)
- **Step 2:** Choose Parameters (checkboxes: Consumption, Peak Demand, Power, Power Factor)
- **Step 3:** Set Date Range (calendar month or custom range)
- **Step 4:** Click "Go" to render

### 2. Interval Control
- **Minute:** Highest granularity, shows individual readings
- **Halfhour:** 30-minute aggregated bars (default)
- **Day:** Daily totals
- **Month:** Monthly totals

### 3. Chart Interactions
- Hover for tooltip with exact value + timestamp
- Edit pencil icon re-opens selection modal for that chart
- Delete trash icon removes the chart panel
- Reload button (↻) refreshes all chart data

### 4. Multi-Chart Stacking
- Multiple parameter charts stack vertically
- Each chart has independent interval control
- Charts share the same date range

---

## Data Points Observed

| Point | Parameters | Period | Interval |
|-------|-----------|--------|----------|
| 3 The Terrace (45829614) | Consumption | Feb 01–24, 2026 | Halfhour |

**Chart Data Range:** 0–60+ kWh per halfhour interval, showing typical commercial consumption patterns with daily cycles (high during business hours, low overnight).

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| GET | `/api/sensing-monitoring/charting` | `point_id`, `parameters[]`, `date_from`, `date_to`, `interval` |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-initial-setup.png` | Selection modal for choosing measurement point and parameters |
| `02-chart-rendered.png` | Rendered consumption chart with halfhour interval over February |

---

## Key Insights

1. **Same charting engine** as Utilities & Services — identical SVG rendering and interval controls
2. **Parameter flexibility** — Multiple parameters can be overlaid or stacked
3. **Point-based selection** — Uses measurement point IDs rather than site-level selection
4. **AI-Ready export** follows the same schema as other reports
5. **Edit-in-place** — Charts can be modified without re-navigating
