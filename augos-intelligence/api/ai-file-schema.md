# Augos AI-Ready File Schema

## Overview

Every report in the Augos platform (except Data Download and Triggers) offers a **"Download AI-Ready File (Beta)"** export. These files are designed for direct ingestion by LLMs (ChatGPT, Gemini, Claude, etc.).

### File Properties

| Property | Value |
|----------|-------|
| **Format** | `.min.json` (minified JSON) |
| **Typical Size** | 38 KB – 454 KB |
| **Encoding** | UTF-8 |
| **Naming Convention** | `{Report} - {Site}_{Point} ({PointID})-{StartDate}-{EndDate}.min.json` |
| **Generation** | Client-side (Blob URL via `URL.createObjectURL`) |
| **Download Trigger** | Banner button → Disclaimer modal (checkbox + download) |
| **Reports With AI File** | 10 of 13 (all except Data Download, Triggers, and Bill Verification*) |

*Bill Verification exports a separate `.json` format without the `_aiInstructions` wrapper.

---

## Universal Structure

Every AI file has exactly two top-level keys:

```json
{
  "_aiInstructions": { ... },
  "data": [ ... ] or { ... }
}
```

---

## `_aiInstructions` — System Prompt Block

**Identical across all reports.** This block provides structured guidance to any AI assistant reading the file.

```json
{
  "_aiInstructions": {
    "summary": "Structured monitoring data exported from the Augos platform.",
    "context": "Data may relate to energy usage, utility billing, environmental conditions, equipment monitoring, or manufacturing metrics.",
    "guidelines": [
      "Base all responses strictly on the data provided in this file unless explicitly instructed otherwise.",
      "Avoid assumptions, estimates, or the use of external sources unless the user clearly asks for them.",
      "Do not generate commentary that is not supported by the supplied data.",
      "If information required to answer a question is not present, state this clearly rather than speculating.",
      "When identifying trends or issues, reference specific values or time periods from the data.",
      "Keep explanations clear, structured, and free of jargon where possible.",
      "Where helpful, present output in bullet points or numbered lists for readability.",
      "Highlight anomalies, inefficiencies, or patterns only if the data supports them.",
      "Maintain a neutral tone and do not offer opinions unless asked to interpret or prioritise."
    ],
    "outputFormatSuggestion": {
      "include": [
        "plain-language summary",
        "supporting data references",
        "recommendations (if relevant)"
      ],
      "structure": "use short paragraphs, bullet points, or tables where appropriate"
    }
  }
}
```

### Guidelines Analysis

| # | Guideline | Purpose |
|---|-----------|---------|
| 1 | Base responses on data only | Prevents hallucination |
| 2 | Avoid assumptions | Ensures data-driven analysis |
| 3 | No unsupported commentary | Accuracy over verbosity |
| 4 | State when data is missing | Transparency over speculation |
| 5 | Reference specific values | Verifiability |
| 6 | Clear, jargon-free | Accessibility for non-technical users |
| 7 | Bullet points/lists | Structured output |
| 8 | Highlight anomalies | Proactive insights |
| 9 | Neutral tone | Objective analysis |

---

## `data` — Report-Specific Schemas

### Pattern A: Array of Arrays (Most Reports)

Used by: **Cost Breakdown**, **Consumption Breakdown**, **Time of Use**

```
data: [
  [metadata_array],      // Array 0: report context
  [summary_array],       // Array 1: high-level summary
  [detail_array],        // Array 2: detailed records
  [sub_detail_array],    // Array 3+: additional detail levels
  ...
]
```

Each inner array is indexed by an `index` field that identifies which "section" of the report it represents.

### Pattern B: Object with Named Keys

Used by: **Power Factor & Demand**, **Downtime Report**

```
data: {
  "key1": [...],
  "key2": [...],
  ...
}
```

---

## Report-Level Schemas

### Cost Breakdown (134 KB, 7 arrays)

| Array | Items | Key Fields | Purpose |
|-------|-------|------------|---------|
| `[0]` | 1 | `tariffReportID, utility, utilityID, tariffScheme, tariffSchemeID, currency` | Tariff metadata |
| `[1]` | 6 | `pointID, tariffType, tariffTypeID, units, rate, measurementUnit, total, percentage, fixed, sequenceID` | Current month line items |
| `[2]` | 73 | `pointID, point, parentID, startDateUTC, monthDescription, tariffTypeID, tariffType, cost, sequenceID` | 12-month trend per tariff type |
| `[3]` | 16 | `pointID, point, parentID, level, thisOne, startDateUTC, endDateUTC, cost, consumption, demand, avgKwh` | Sub-measurement hierarchy (current month) |
| `[4]` | 97 | `pointID, parentID, item, tariffTypeID, measurementUnit, units, rate, total, totalAmount, percentage` | Detailed line items per sub-point |
| `[5]` | 216 | `pointID, parentID, startDateUTC, endDateUTC, monthDescription, cost, dateRowID` | 12-month trend per sub-point |
| `[6]` | 198 | `startDateUTC, endDateUTC, monthDescription, cost, consumption, maxDemand, avgKwh` | Full historical trend (Jul 2009 → Feb 2026) |

**Scale:** One & Only Cape Town has **16.5 years** of historical cost data in a single file.

---

### Consumption Breakdown (264–454 KB, 6 arrays)

| Array | Items | Key Fields | Purpose |
|-------|-------|------------|---------|
| `[0]` | 7-12 | `pointID, point, fullDescription, parentID, level, consumption` | Hierarchy tree (point structure) |
| `[1]` | 1,130-1,920 | `pointID, point, fullDescription, parentID, level, interval` | Detailed time-series (per-point, per-interval) |
| `[2]` | 24-40 | Same structure | Daily aggregates |
| `[3]` | 3-10 | Same structure | Monthly aggregates |
| `[4]` | 10-12 | `pointID, point, serialNo, start, end, consumption` | Meter summary |
| `[5]` | 1 | `unit` | Units metadata (e.g., "kWh") |

**Largest file type** at 454 KB — most granular interval data.

---

### Time of Use (38 KB, 6 arrays)

| Array | Items | Key Fields | Purpose |
|-------|-------|------------|---------|
| `[0]` | 1 | `currency, index` | Currency metadata |
| `[1]` | 3 | `tariffType, units, percentageUnits, cost, percentageCost, tariffReportID` | TOU summary (Peak/Standard/Off-peak) |
| `[2]` | 168 | `tariffTypeID, tariffType, tick, day, time, units` | Heatmap data (24hr × 7 days × tariff types) |
| `[3]` | 13 | `tariffReportID, period, startDateUTC, endDateUTC, season, standardUnits` | Period breakdown |
| `[4]` | 7 | `PointId, day, averageComsumption, index` | Daily average profile |
| `[5]` | 26 | `dayDate, pointID, standardUnits, offpeakUnits, peakUnits, cost` | Daily breakdown log |

**Most compact** analytical file — efficient TOU segmentation.

---

### Power Factor & Demand (313 KB, Object pattern)

| Key | Items | Key Fields | Purpose |
|-----|-------|------------|---------|
| `tariffReportID` | — | Integer | Report identifier |
| `details` | 36 | Mixed | Detail records |
| `firstChart` | 24 | Time-series | Peak demand trend (24 months) |
| `tails` | 4 | KPI values | Summary KPI cards |
| `secondChart` | 72 | Time-series | Power factor trend |
| `pieChart` | 24 | Contribution data | Donut chart data |
| `summary` | 24 | Monthly summary | Performance table |
| `summaryDetail` | 72 | Detail breakdown | Expanded performance data |

**Only report using named object keys** instead of indexed arrays.

---

### Bill Verification (12 KB, different structure)

```json
{
  "data": [...],    // 25 comparison records
  "count": 25       // Total record count
}
```

**Note:** Does NOT include `_aiInstructions`. Uses a simpler wrapper with `data` + `count`.

---

## File Size Comparison

| Report | Example Size | Data Density |
|--------|-------------|--------------|
| **Consumption Breakdown** | 454 KB | Highest — full interval data for all sub-points |
| **Power Factor & Demand** | 313 KB | 24-month charts + KPIs + performance table |
| **Consumption Breakdown** | 264 KB | Smaller hierarchy (fewer sub-points) |
| **Cost Breakdown (One&Only)** | 134 KB | 16.5 years of cost history |
| **Cost Breakdown (Tiger)** | 64 KB | Fewer sub-points, same structure |
| **Time of Use** | 38 KB | Most compact — efficient TOU data |
| **Bill Verification** | 12 KB | Comparison records only |

---

## Download Flow (UX)

```
1. User clicks "Download AI-Ready File (Beta)" banner
   ↓
2. Modal appears: "Augos Intelligence"
   - Disclaimer text about data sensitivity
   - Checkbox: "I have read and accept the Data Sensitivity and AI Output Disclaimer"
   ↓
3. User checks checkbox → "Download AI File" button enables
   ↓
4. Click download → Browser generates Blob URL → File downloads
   ↓
5. File lands in Downloads as: {Report} - {Site} ({ID})-{Date Range}.min.json
```

---

## Reports Without AI File

| Report | Reason |
|--------|--------|
| **Data Download** | Already provides raw CSV/Excel export |
| **Triggers** | Configuration tool, not a data report |
| **Charting** | Has AI file (despite being a visualization tool) |

---

## LLM Usage Recommendations

Based on the embedded `_aiInstructions`:

1. **Feed the entire file** — Files are designed as self-contained data packages (30–450 KB is within all LLM context windows)
2. **Ask analytical questions** — "What are the cost trends?", "Which months had the highest demand?"
3. **Request comparisons** — "Compare peak vs off-peak consumption"
4. **Flag anomalies** — "Are there any unusual patterns?"
5. **Generate summaries** — "Summarize this cost data for a board presentation"

---

*Documented: 23 Feb 2026*
*Source files: 10 AI exports from Downloads folder*
*Covering: Cost Breakdown, Consumption Breakdown, Time of Use, Power Factor & Demand, Bill Verification*
