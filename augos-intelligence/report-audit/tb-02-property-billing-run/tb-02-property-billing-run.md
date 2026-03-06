# TB-02: Property Billing Run

> **Module:** Tenant Billing  
> **URL:** `live.augos.io/app/property-billing-run`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Property Billing Run report provides the most granular financial analysis in the Tenant Billing module. It breaks down billing at the property → unit → tenant → tariff level, showing exact consumption, demand, rates, and amounts across Primary, Backup, Green, and Total supply categories. This is the report used by billing administrators to validate and audit tenant invoices.

---

## Page Layout

### Header Bar
| Element | Description |
|---------|-------------|
| **Page Title** | "Property Billing Run" with blue left-border accent |
| **Property Selector** | Autocomplete dropdown (e.g., "Cape Town Market Site Total (36040590)") with clear (×) button |
| **Navigation Arrows** | `←` `→` buttons to cycle through properties |

### Utility Tabs
| Tab | Description |
|-----|-------------|
| **Electricity** (active, blue) | Electricity billing data |
| **Water** | Water billing data |
| **+ Add measurement** | Adds a new measurement type |

### Date Selector
| Element | Value |
|---------|-------|
| **Calendar Month** | "January 2026" button |
| **From** | `2026/01/01 00:00` |
| **To** | `2026/01/31 23:59` |
| **Three-dot menu** (⋮) | Additional date options |

### Billing Summary Table

#### Top-Level Columns
| Column Group | Sub-Columns |
|-------------|-------------|
| **Unit** | Unit name + ID |
| **Tenant** | Tenant name |
| **Value (ZAR)** | Revenue, Cost, Over/Under, % |
| **Consumption (kWh)** | Recovered |
| **Demand (kVA)** | Recovered |

#### Observed Data
| Unit | Tenant | Revenue | Cost | Over/Under | % | Consumption | Demand |
|------|--------|---------|------|------------|---|-------------|--------|
| Fruit & Veg (47537682) | Fruit & Veg | 135,448.74 | 348,820.99 | -213,372.25 | -157.53 | 47,014.86 | 0 |
| M & R Nutripick (47537577) | M & R Nutripick | 183,349.91 | 913,019.77 | -729,669.86 | -397.97 | 64,130.98 | 0 |
| **Total** | | **318,798.65** | **1,261,840.76** | **-943,042.11** | **-295.81** | **111,145.84** | **0** |

### Expanded Tariff Breakdown
When a unit row is expanded, it shows a **Tariff Type breakdown table** with:

| Column Group | Fields |
|-------------|--------|
| **Tariff Type** | Row label (e.g., "Consumption - standard", "Consumption - standard (Common)", "Monthly service charge") |
| **Primary** | Units, Rate (ZAR), Amount (ZAR) |
| **Backup** | Units, Rate (ZAR), Amount (ZAR) |
| **Green** | Units, Rate (ZAR), Amount (ZAR) |
| **Total** | Units, Rate (ZAR), Amount (ZAR) |

#### Tariff Breakdown Example (Fruit & Veg)
| Tariff Type | Primary Units | Primary Rate | Primary Amount | Total Units | Total Rate | Total Amount |
|-------------|---------------|-------------|----------------|-------------|-----------|--------------|
| Consumption - standard | 10,564.39 | 2.7986 | 29,565.51 | 10,564.39 | 2.7986 | 29,565.51 |
| Consumption - standard (Common) | 36,450.46 | 2.7986 | 102,010.27 | 36,450.46 | 2.7986 | 102,010.27 |
| Monthly service charge | 1 | 3,872.9500 | 3,872.95 | 1.00 | 3,872.9500 | 3,872.95 |
| **Total** | | | **135,448.74** | | | **135,448.74** |

### Pagination
- `Rows per page: 25 ▼`
- `1–2 of 2` with `<` `>` navigation

---

## Functional Components

### 1. Property Selector
- **Type:** Autocomplete with search and navigation arrows
- **Behavior:** Loads billing data for the selected property
- **Arrow Navigation:** Cycles through properties alphabetically

### 2. Utility Tabs
- Electricity/Water toggle
- Independent billing data per utility type

### 3. Unit Expansion
- Accordion-style expansion of unit rows
- Reveals full tariff-level breakdown with multi-column grouped headers

### 4. Multi-Supply Categories
- **Primary:** Standard grid supply
- **Backup:** Generator/backup power supply
- **Green:** Renewable/solar supply
- **Total:** Combined across all supply types

### 5. Over/Under Analysis
- Shows difference between Revenue and Cost per unit
- Negative values indicate under-recovery (loss)
- Percentage shows recovery efficiency

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| GET | `/api/property-billing-run` | `property_id`, `month`, `year`, `utility_type` |
| GET | `/api/property-billing-run/{property_id}/tariff-breakdown` | `unit_id`, `month`, `year` |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-billing-run.png` | Initial billing run view with property selector |
| `02-tariff-breakdown.png` | Expanded unit showing tariff type breakdown with Primary/Backup/Green/Total columns |

---

## Key Insights

1. **Most data-dense report** in the entire platform — 4×3 tariff matrix per unit
2. **Multi-supply billing** — Primary/Backup/Green categories suggest embedded generation support
3. **Common area allocation** — "Consumption - standard (Common)" tariff shows common area cost recovery
4. **Monthly service charges** — Fixed fees alongside consumption-based charges
5. **Under-recovery flagging** — Negative Over/Under values highlighted for billing review
6. **This is the invoice validation tool** — Billing admins use this to verify tenant statements
