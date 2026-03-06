# Cost Allocation

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/cost-allocation?pointId=47688315&productId=1` |
| **Purpose** | Allocate measured electricity costs to individual business units, departments, or tenants based on sub-meter consumption and demand. |
| **Primary Users** | Finance Teams, Property Management, Multi-tenant Operators, Cost Centre Managers |
| **Fuel Types** | Electricity (primary — tariff-dependent) |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

**Note:** This report was audited using **Babylonstoren|Simondium (47688315)** as the primary site has this feature configured with 17 business units. One & Only Cape Town (8323) does not have Cost Allocation configured.

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Cost Allocation — Babylonstoren|Simondium (47688315)"

### 2. Date Range Controls
- **Manual pickers:** From 2026/02/01 00:00 / To 2026/02/28 23:59
- **No preset buttons** (unlike other reports) — only manual date range
- **Note:** No fuel selector visible — this is an Electricity-only report

### 3. AI Banner
- Purple gradient with "Download AI-Ready File (Beta)" CTA

### 4. Cost Distribution Bar (★ Distinctive)
- **Type:** Horizontal stacked percentage bar with 17 color-coded segments
- **Each segment** represents a business unit's share of total cost
- **Legend:** Three-row legend mapping colors to business unit names and point IDs
- **Sample segments:** BAB02 (20%), BAB15 (17%), BTT06 (18%), BTT07 (23%)

### 5. Cost Allocation Table
- **Header:** Blue banner "Cost allocation" with collapse toggle
- **Columns:**

| Column | Description | Example |
|--------|-------------|---------|
| ⊕ / ⊖ | Expand/collapse row | Green + / red - |
| Business Unit | Sub-meter name and point ID | Babylonstoren - BAB02 (49638618) |
| Consumption (kWh) | Total consumption for period | 39,898 |
| Peak Demand (kVA) | Maximum demand | 305.4 |
| Cost (ZAR) | Calculated cost for this unit | 318,372 |
| Adjustment (ZAR) | Manual adjustments | 0 |
| Allocation (ZAR) | Final allocated cost (Cost + Adjustment) | 318,372 |
| Status | Alert/warning icon | ⚠️ |
| % | Percentage bar with value | 🟧 20% |

**All 17 business units (Feb 2026):**

| Business Unit | Consumption (kWh) | Peak Demand (kVA) | Cost (ZAR) | Allocation (ZAR) | % |
|--------------|-------------------|-------------------|-----------|------------------|---|
| BAB02 | 39,898 | 305.4 | 318,372 | 318,372 | 20% |
| BAB03 | 10,678 | 0 | 41,992 | 41,992 | 3% |
| BAB05 | 863 | 0 | 3,788 | 3,788 | 0% |
| BAB15 | 18,753 | 326.4 | 265,644 | 265,644 | 17% |
| BAB17 | 1,165 | 0 | 4,804 | 4,804 | 0% |
| BTP01 | 8,903 | 0 | 27,656 | 27,656 | 2% |
| BTP03 | 15,214 | 0 | 32,941 | 32,941 | 2% |
| BTP04 | 6,218 | 0 | 28,161 | 28,161 | 2% |
| BTP05 | 1,024 | 0 | 32,941 | 32,941 | 2% |
| BTT01 | 15,306 | 0 | 32,941 | 32,941 | 2% |
| BTT04 | 13,970 | 0 | 53,484 | 53,484 | 3% |
| BTT06 | 115,004 | 169.9 | 280,723 | 280,723 | 18% |
| BTT07 | 125,138 | 268.2 | 375,532 | 375,532 | 23% |
| BTT08 | 4,983 | 0 | 19,167 | 19,167 | 1% |
| BTT09 | 19,766 | 0 | 78,776 | 78,776 | 5% |
| BTT10 | 119 | 0 | 620 | 620 | 0% |
| BTT14 | 161 | 0 | 835 | 835 | 0% |
| **Total** | **397,162** | **1,069.9** | **1,598,376** | **1,598,376** | **100%** |

### 6. Expanded Row Detail (★ Distinctive)
When a row's ⊕ button is clicked, it expands to show tariff-level breakdown:

| Item | Units | Unit | Cost/Unit (ZAR) | Cost (ZAR) |
|------|-------|------|----------------|-----------|
| Consumption - standard | 13,069.9 | /kWh | 3.77 | 49,230 |
| Consumption - peak | 9,526.6 | /kWh | 7.85 | 74,800 |
| Consumption - off-peak | 28,843.2 | /kWh | 2.43 | 70,167 |
| Demand charge | 305.5 | /kVA | 254.76 | 77,835 |

This "bill-behind-the-allocation" view shows exactly how the tariff rates were applied to each unit's measured consumption.

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Date From/To | DateTime pickers | Manual entry | Current month |
| Row expand/collapse | ⊕/⊖ buttons | Per row | Collapsed |

---

## Downloads & Exports

| Export | Format | Trigger | Content |
|--------|--------|---------|---------|
| AI-Ready File | JSON | Banner button | Complete allocation data |

**Note:** No explicit XLSX/CSV export buttons visible on this report — unlike Cost Breakdown and Bill Verification.

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| Multi-unit cost allocation | ✅ 17 business units | ❌ |
| Distribution bar (per unit) | ✅ Color-coded % bar | Cost Breakdown has charge-type bar |
| Expandable row detail | ✅ Tariff-level breakdown per unit | ❌ |
| Adjustment column | ✅ Manual cost adjustments | ❌ |
| Status indicators | ✅ ⚠️ per row | ❌ |
| No fuel selector | ✅ (Electricity only) | Most have multi-fuel |
| Configuration-dependent | ✅ Requires setup | Most are auto-populated |

---

## Configuration States

| State | Description |
|-------|-------------|
| **Not Configured** | Shows "Cost Allocation has not been set up for this site" + "SET UP COST ALLOCATION" button (seen on One & Only Cape Town) |
| **Configured** | Full distribution bar + allocation table with expandable rows (seen on Babylonstoren) |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **How is the bill distributed?** — Distribution bar and table show each unit's share of total cost.
2. **Which units consume the most?** — Consumption and % columns immediately rank units (BTT07 at 23% leads Babylonstoren).
3. **What tariff rates apply per unit?** — Expanded row shows exact ZAR/kWh per TOU period and ZAR/kVA for demand.
4. **Are there manual adjustments?** — Adjustment column tracks any overrides.
5. **What's the total site cost?** — Total row: 397,162 kWh / 1,598,376 ZAR for Feb 2026.

---

## Screenshots

### One & Only | Cape Town (8323) — Not Configured
| # | File | Description |
|---|------|-------------|
| 01 | `01-not-configured.png` | Empty state: "Cost Allocation has not been set up for this site" with setup CTA |

### Babylonstoren|Simondium (47688315) — Fully Configured
| # | File | Description |
|---|------|-------------|
| 02 | `02-distribution-bar-and-table-top.png` | Distribution bar (17 units), allocation table header and first 6 units |
| 03 | `03-all-units-and-totals.png` | Remaining units (BAB17 through BTT14) and Total row (1,598,376 ZAR) |
| 04 | `04-expanded-row-tariff-detail.png` | BAB02 expanded showing TOU line items: standard (3.77/kWh), peak (7.85/kWh), off-peak (2.43/kWh), demand (254.76/kVA) |

---

*Audited: 23 Feb 2026*
*Sites: One & Only | Cape Town (8323) — not configured, Babylonstoren|Simondium (47688315) — fully configured*
*Date range: February 2026*
