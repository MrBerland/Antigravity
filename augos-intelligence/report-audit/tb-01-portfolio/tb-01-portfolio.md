# TB-01: Portfolio

> **Module:** Tenant Billing  
> **URL:** `live.augos.io/app/portfolio`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Portfolio report is the executive-level financial dashboard for the Tenant Billing module. It provides a consolidated view of all properties in the portfolio with revenue, cost, profit/loss, and recovery rate metrics. This is the primary entry point for understanding the financial health of the entire billing operation.

---

## Page Layout

### Header Bar
| Element | Description |
|---------|-------------|
| **Page Title** | "Portfolio" with blue left-border accent |

### Utility Tabs
| Tab | Description |
|-----|-------------|
| **Portfolio** (active) | Shows combined utility view |
| **Electricity** | Filters to electricity billing only |
| **Water** | Filters to water billing only |
| **+ Add measurement** | Adds a new measurement type |

### Date Selector
- Calendar icon with month selector (e.g., "January 2026")
- Three-dot menu (⋮) for additional options

### Portfolio Financial Table

| Column | Description |
|--------|-------------|
| **Property** | Property name + ID (e.g., "Urban Growth\|Park (Paarl) (10457)") |
| **Recovery Rate** | Decimal ratio — revenue ÷ cost (e.g., 0.79, 1.00, 2.39) |
| **Revenue** (ZAR) | Total revenue billed to tenants |
| **Cost** (ZAR) | Total cost from utility provider |
| **Profit / Loss** (ZAR) | Revenue minus Cost — **red** for losses, **white** for gains |
| **Status** | Billing status (e.g., "In progress") |
| **Expand (+)** | Expands to show utility-level breakdown |

### Properties Observed

| # | Property | Recovery Rate | Revenue | Cost | Profit/Loss | Status |
|---|----------|--------------|---------|------|-------------|--------|
| 1 | Urban Growth\|Park (Paarl) (10457) | 0.79 | 380,853.79 | 413,747.06 | -32,893.26 | In progress |
| 2 | Marriott\|Protea Hotels\|Sea Point (14426) | 0.20 | 59,992.77 | 270,385.79 | -210,393.02 | In progress |
| 3 | Sun International\|Grand West (14546) | 0.00 | 779,240.76 | 361,784.44 | 417,456.32 | In progress |
| 4 | Work Spectrum (17635) | 1.00 | 31,746.78 | 4,771.81 | 26,974.97 | In progress |
| 5 | Cape Town Market Site Total (36040590) | 0.24 | 322,667.39 | 1,261,840.77 | -939,173.38 | In progress |
| 6 | Forlee Holdings\|Sherwood Centre\|Mains (49061068) | 1.90 | 63,268.86 | 24,027.42 | 39,241.44 | In progress |
| 7 | Forlee Holdings\|Fiveways Centre\|Mains (49061073) | 2.39 | 208,268.76 | 79,408.15 | 128,860.61 | In progress |
| 8 | Old Mutual\|Pinelands HO (51292506) | 0.01 | 22,992.43 | 2,969,783.96 | -2,946,791.53 | In progress |
| **Total** | | **6.53** | **1,869,031.54** | **5,385,749.40** | **-3,516,717.86** | |

### Expanded Property Row
When clicking the (+) icon, a utility breakdown appears:
- Shows Electricity and Water as separate rows
- Each utility row has its own Revenue, Cost, and Profit/Loss

---

## Charts & Visualizations

### Performance Chart (Bottom Left)
- **Title:** "Portfolio"
- **Type:** Dual-axis chart
- **Left Y-Axis:** ZAR (millions) — Revenue vs Cost bars
- **Right Y-Axis:** Recovery % — Line overlay
- **X-Axis:** Rolling 13-month period
- **Data:** Bar chart shows monthly Revenue (blue) and Cost (red) with Recovery % line

### Summary Cards (Bottom Right)
| Card | Value | Details |
|------|-------|---------|
| **Profit / Loss** | -3,397,335.47 (ZAR) | Large display with sparkline trend |
| **Recovery Trend** | 2.25% ↑ | Green upward indicator showing improvement |

---

## Functional Components

### 1. Utility Filtering
- Toggle between Portfolio (combined), Electricity, and Water views
- Each view recalculates all financial metrics

### 2. Calendar Month Selector
- Selects the billing month to view
- All properties show data for the same month

### 3. Property Expansion
- (+) button expands to show utility-level breakdown
- Collapsed by default for clean overview

### 4. Add Measurement
- Allows adding new utility measurement types to the portfolio

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| GET | `/api/portfolio` | `month`, `year`, `utility_type` |
| GET | `/api/portfolio/chart` | `months_back` |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-portfolio-overview.png` | Full portfolio table with 8 properties, financial metrics, and status |
| `02-portfolio-charts.png` | Performance chart and Profit/Loss summary card |
| `03-property-expanded.png` | Property row expanded showing electricity/water breakdown |

---

## Key Insights

1. **Executive dashboard** — High-level financial health at a glance
2. **Recovery Rate** is the key KPI — Shows how much of the cost is being recovered through tenant billing
3. **Significant portfolio losses** — Total -3.5M ZAR indicates billing configuration issues or common area costs
4. **Old Mutual outlier** — 0.01 recovery rate suggests bulk supply or common area metering without tenant billing
5. **Profit/Loss color coding** — Red for losses provides immediate visual alerting
6. **13-month rolling chart** — Allows trend analysis across annual billing cycles
