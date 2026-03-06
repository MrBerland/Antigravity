# Augos API Reference — Utilities & Services

## Overview

All Augos report pages consume a RESTful JSON API. This document maps every endpoint used by the 13 Utilities & Services reports.

**Base URL:** `https://dev.live.augos.io`  
**Authentication:** Cookie-based session token (`token=...`)  
**Response Format:** JSON  
**Caching:** ETag + 304 Not Modified  

---

## Common Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `pointID` | Integer | Measurement point identifier | `8323` |
| `startDateUTC` | String (ISO date) | Period start date | `2026-01-01` |
| `endDateUTC` | String (ISO date) | Period end date | `2026-01-31` |
| `productTypeID` | Integer | Product type (2 = Electricity) | `2` |
| `billing` | Integer | Billing mode flag | `0` |
| `offset` | Integer | UTC timezone offset in minutes | `-120` |
| `date` | String (ISO date) | Specific date reference | `2026-02-23` |

---

## Endpoints by Report

### 1. Dashboard
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/dashboard` |
| **Key Params** | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| **Response** | Summary KPI data, trend data for consumption/cost/demand charts |
| **Notes** | Aggregates data from multiple sub-endpoints for the dashboard widgets |

---

### 2. Technical Analysis
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/technical-analysis` |
| **Key Params** | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| **Response** | Time-series demand data, meter list, statistical analysis |
| **Notes** | Statistics toggle triggers client-side computation, no separate API call |

---

### 3. Consumption Breakdown
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/consumption-breakdown` |
| **Key Params** | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| **Response** | Hierarchical point data (parent/child), consumption totals, % contribution |
| **Notes** | Returns tree structure for hierarchy view, flat data for charts |

---

### 4. Cost Breakdown ✅ (Verified via interceptor)
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/cost-breakdown` |
| **Key Params** | `pointID=8323`, `startDateUTC=2026-01-01`, `endDateUTC=2026-01-31`, `productTypeID=2`, `billing=0` |
| **Response Size** | ~65 KB |
| **Response Structure** | Array of arrays: `[[metadata], [line_items], ...]` |

#### Response Schema (Captured)

**Element 0 — Metadata:**
```json
{
  "tariffReportID": 184106,
  "utility": "City of Cape Town",
  "utilityID": 5029,
  "tariffScheme": "Large Power User (Medium Voltage) TOU",
  "tariffSchemeID": 11191,
  "currency": "ZAR",
  "index": 0
}
```

**Element 1+ — Line Items:**
```json
{
  "pointID": 8323,
  "tariffType": "Consumption - standard",
  "tariffTypeID": 56,
  "units": 231071.5625,
  "rate": 2.1708,
  "measurementUnit": "/kWh",
  "total": 501610.15625,
  "percentage": 36.304,
  "fixed": 2,
  "sequenceID": 1,
  "index": 1
}
```

**Tariff Types Observed:**
| tariffType | tariffTypeID | measurementUnit | Example Rate (ZAR) |
|------------|-------------|-----------------|---------------------|
| Consumption - standard | 56 | /kWh | 2.1708 |
| Consumption - standard (feed in) | 11 | /kWh | 1.1517 |
| Consumption - peak | 36 | /kWh | 3.3396 |
| Consumption - off-peak | 37 | /kWh | 1.7563 |

---

### 5. Cost Allocation
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/cost-allocation` |
| **Key Params** | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| **Response** | Cost distribution per sub-measurement point, tariff detail |
| **Notes** | Returns "not configured" state if allocation rules not set up |

---

### 6. Bill Verification
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/bill-verification` |
| **Key Params** | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| **Response** | Trend data, comparison records (calculated vs billed) |
| **Notes** | Returns empty state if no billing data configured |

---

### 7. Power Factor & Demand ✅ (Verified via network monitor)
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/power-factor-demand` |
| **Key Params** | `pointID`, `startDateUTC`, `endDateUTC` |
| **Response** | 24-month trend data for Peak Demand, Power Factor, and Reactive Power |
| **Notes** | No `productTypeID` required — electricity-only report |

---

### 8. Time of Use ✅ (Verified via network monitor)
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/electricity/time-of-use` |
| **Key Params** | `pointID`, `startDateUTC`, `endDateUTC` |
| **Response** | Time-series data segmented by tariff periods (Peak, Standard, Off-Peak) |
| **Notes** | Under `/electricity/` namespace — electricity-specific endpoint |

---

### 9. Tariff Comparison ✅ (Verified via network monitor)
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/electricity/tariff-comparison` |
| **Key Params** | `pointID` |
| **Response** | Comparative cost analysis across multiple tariff schemes |
| **Notes** | Under `/electricity/` namespace. May have additional date params |

---

### 10. Load Curtailment ✅ (Verified via network monitor)
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/load-curtailment/get-load-curtailment` |
| **Key Params** | `pointID`, `date`, `offset=-120` |
| **Response** | Real-time compliance data, Stage info, Curtailment Base Load (CBL) |
| **Notes** | Uses `date` (single) rather than start/end range. `offset` is UTC timezone offset. Nested under `/load-curtailment/` |

---

### 11. Charting
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/charting` or `/api/v1/data` (parameter-dependent) |
| **Key Params** | `pointID`, `startDateUTC`, `endDateUTC`, `parameterID`, `resolution` |
| **Response** | Time-series chart data for selected parameters |
| **Notes** | Dynamic — one API call per selected parameter. Resolution param matches tab selection (min/halfhour/day/month) |

---

### 12. Data Download
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/data-download` |
| **Key Params** | `pointID`, `startDateUTC`, `endDateUTC`, `format` (csv/xlsx), `phase` (by_phase/summed) |
| **Response** | Binary file download (CSV or XLSX) |
| **Notes** | Returns file directly, not JSON. No preview — triggers browser download |

---

### 13. Triggers
| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **Endpoint** | `/api/v1/triggers` |
| **Key Params** | `page`, `pageSize` (pagination) |
| **Response** | Paginated list of trigger configurations |
| **Notes** | Organization-wide — ignores pointID. Returns all 342 triggers with CRUD support |

---

## API Patterns

### Namespace Structure
```
/api/v1/
├── dashboard
├── technical-analysis
├── consumption-breakdown
├── cost-breakdown
├── cost-allocation
├── bill-verification
├── power-factor-demand
├── electricity/
│   ├── time-of-use
│   └── tariff-comparison
├── load-curtailment/
│   └── get-load-curtailment
├── charting (or /data)
├── data-download
└── triggers
```

### Response Patterns

| Pattern | Reports Using It |
|---------|-----------------|
| **Array of arrays** `[[metadata], [data_rows]]` | Cost Breakdown, Cost Allocation |
| **Single JSON object** with nested arrays | Dashboard, Technical Analysis, Time of Use |
| **Flat array** of records | Consumption Breakdown, Triggers |
| **Binary file** (download) | Data Download |

### Authentication Flow
1. Login POST to `/api/auth/login` with email/password
2. Receives session token in cookie
3. All subsequent API calls include cookie automatically
4. Token has expiry — session timeout causes redirect to `/login`

---

## Key Technical Findings

1. **ETag caching** — The API uses `ETag` headers and responds with `304 Not Modified` when data hasn't changed, reducing bandwidth significantly.
2. **Consistent naming** — API slugs match URL slugs exactly (e.g., `/cost-breakdown` in URL → `/api/v1/cost-breakdown`).
3. **Electricity namespace** — Reports specific to electricity (TOU, Tariff Comparison) sit under `/api/v1/electricity/`.
4. **Load Curtailment** — Uses different parameter pattern (`date` + `offset` vs `startDateUTC` + `endDateUTC`), reflecting its real-time nature.
5. **Triggers** — Organization-wide scope, ignoring the `pointID` URL parameter.

---

*Captured: 23 Feb 2026*  
*Method: Fetch/XHR interceptor injection + Browser DevTools network monitoring*
