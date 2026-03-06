# SM-03: Data Download

> **Module:** Sensing & Monitoring  
> **URL:** `live.augos.io/app/sensing-and-monitoring/data-download`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Data Download report provides a streamlined interface for exporting raw sensor data in bulk. Users select a measurement point, configure interval/phase/format parameters, choose a date range, and download the file. This is designed for data analysts and engineers who need raw data for external tools.

---

## Page Layout

### Header Banner
- Blue gradient banner with download icon (⬇) and title "Download"

### Two-Pane Configuration

#### Left Pane: Select Measurement
| Element | Description |
|---------|-------------|
| **Section Title** | "Select Measurement" in blue |
| **Point Selector** | Autocomplete dropdown with clear (×) button |
| **Selected Value** | Shows point name + ID (e.g., "3 The Terrace (45829614)") |

#### Right Pane: Select Parameters
| Element | Description |
|---------|-------------|
| **Section Title** | "Select Parameters" in blue |
| **Interval** | Button group: `Minute` · `Halfhour` · `Day` · `Month` |
| **Phase** | Radio buttons: `By Phase` · `Summed` |
| **Format** | Radio buttons: `CSV` · `Excel` |

### Footer Controls
| Element | Description |
|---------|-------------|
| **Quick Date Buttons** | `Last 7 days` · `Feb 26` · `Jan 26` · `Dec 25` · `Nov 25` · `More` |
| **From/To Fields** | Datetime inputs: `2026/02/17 00:00` → `2026/02/24 23:59` |
| **Download Button** | Grey/disabled until fully configured, then active |

---

## Functional Components

### 1. Measurement Point Selector
- **Type:** Autocomplete with search
- **Behavior:** Single selection with clear button
- **Required:** Yes — must be selected before download

### 2. Interval Configuration
- **Minute:** Raw minute-level readings
- **Halfhour:** Aggregated to 30-minute intervals (default)
- **Day:** Daily summaries
- **Month:** Monthly summaries

### 3. Phase Configuration
- **By Phase:** Downloads data split by electrical phase (Red/White/Blue or L1/L2/L3)
- **Summed:** Downloads total/combined values only

### 4. Format Selection
- **CSV:** Comma-separated values for universal compatibility
- **Excel:** .xlsx format with formatting

### 5. Date Range
- Quick-select buttons auto-populate From/To
- "More" opens the dual calendar date range picker
- Manual date entry in `YYYY/MM/DD HH:MM` format

---

## Data Points Observed

| Configuration | Value |
|--------------|-------|
| Selected Point | 3 The Terrace (45829614) |
| Default Interval | Minute |
| Default Phase | By Phase |
| Default Date Range | Last 7 days |

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| POST | `/api/sensing-monitoring/download` | `point_id`, `interval`, `phase`, `format`, `date_from`, `date_to` |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-initial.png` | Empty state before measurement point selection |
| `02-configured.png` | Fully configured with point selected and parameters set |

---

## Key Insights

1. **Identical to Utilities & Services Data Download** — Same layout, controls, and export patterns
2. **Phase-level granularity** — Critical for three-phase power analysis
3. **Minute-level data available** — Highest resolution data export across the platform
4. **Simple workflow** — Select → Configure → Download — no preview step
5. **No AI-Ready export on this page** — AI export is on Charting/Sensors instead
