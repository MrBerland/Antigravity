# Data Download

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/data-download?pointId=8323&productId=1` |
| **Purpose** | Bulk raw data export tool. Lets users select a measurement point, configure output parameters (phase, format), set a date range, and download raw metering data as CSV or Excel files. A utility tool, not a visualization report. |
| **Primary Users** | Energy Managers, Engineers, Data Analysts, Billing Departments |
| **Fuel Types** | All (point-dependent) |
| **AI File** | ❌ No AI-Ready File option |

---

## Page Layout (Top → Bottom)

### 1. Header Banner
- **Blue banner** with download icon (↓) and title "Download"
- Full-width, matches blue section banner pattern used across the platform

### 2. Configuration Panel (★ Single-Page Tool)

The entire page is a single configuration form — no charts, no tables, no data preview.

**Left Column: Select Measurement**
- **Title:** "Select Measurement" (blue text)
- **Input:** "Select Measurement Point" dropdown/autocomplete
- **Behavior:** Search across all accessible measurement points

**Right Column: Select Parameters**
- **Title:** "Select Parameters" (blue text)

| Parameter | Type | Options | Default |
|-----------|------|---------|---------|
| **Phase** | Radio buttons | By Phase / Summed | None selected |
| **Format** | Radio buttons | CSV / Excel | None selected |

### 3. Date Range Bar (Bottom, Fixed)
- **Quick date buttons:** Last 7 days (active, blue) | Feb 26 | Jan 26 | Dec 25 | Nov 25 | More
- **Manual inputs:**
  - From: `2026/02/16 00:00`
  - To: `2026/02/23 23:59`
- **Download button** (right side, greyed out until all options selected)

---

## Components

### Measurement Point Selector
- **Type:** Autocomplete search dropdown
- **Searches across:** All measurement points in the user's accessible hierarchy
- **Displays:** Point name and ID

### Phase Toggle
- **"By Phase"** — Downloads individual phase data (R, W, B / L1, L2, L3)
- **"Summed"** — Downloads total/aggregate values only

### Format Toggle
- **CSV** — Comma-separated values file
- **Excel** — .xlsx format with formatted columns

### Date Range Selector
- **Quick presets:** Last 7 days, specific months (rolling 4 months + "More")
- **Custom range:** From/To datetime pickers

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Measurement Point | Autocomplete dropdown | All accessible points | Empty |
| Phase | Radio buttons | By Phase, Summed | None |
| Format | Radio buttons | CSV, Excel | None |
| Date Range | Quick buttons + manual inputs | Presets + custom | Last 7 days |
| Download | Action button | Triggers file download | Disabled until configured |

---

## Downloads & Exports

| Export | Format | Trigger | Content |
|--------|--------|---------|---------|
| Data Download | CSV | Download button (after selecting CSV) | Raw metering data for selected point/phase/period |
| Data Download | XLSX | Download button (after selecting Excel) | Same data in Excel format |

**Note:** This is the ONLY report that is purely a download tool — no visualization, no tables, no charts. Its sole purpose is bulk data export.

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| No charts or tables | ✅ Pure configuration → download | ❌ All others display data |
| Phase selection (By Phase / Summed) | ✅ Unique to this tool | ❌ |
| Format selection (CSV / Excel) | ✅ Two formats | Others: XLSX/CSV as inline exports |
| Quick date presets (Last 7 days, monthly) | ✅ Convenient quick buttons | ❌ Others use standard date pickers |
| No AI-Ready file | ✅ Raw data only | Most others have AI file option |
| No page title in standard format | ✅ Uses blue banner instead | ❌ Standard header with title |
| Available in both U&S and S&M modules | ✅ Cross-module tool | ❌ Most reports are module-specific |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required — likely triggers a direct file download from API*

---

## Key Insights This Report Provides

1. **Bulk data access** — The primary tool for exporting raw metering data for external analysis (Excel modeling, ERP import, etc.).
2. **Phase-level granularity** — "By Phase" option gives individual phase data critical for power quality analysis.
3. **Quick historical access** — Preset buttons allow instant download of last 7 days or specific months without manual date entry.
4. **Format flexibility** — CSV for data pipelines, Excel for business users.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-download-config.png` | Full page showing blue "Download" banner, Select Measurement dropdown, Phase and Format radio buttons |
| 02 | `02-date-range-and-download.png` | Scrolled view showing date range presets (Last 7 days, monthly), From/To inputs, Download button |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Note: This is a configuration/download tool, not a visualization report*
