# Tariff Comparison

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/tariff-comparison?pointId=8323&productId=1` |
| **Purpose** | Compare the cost of the current tariff scheme against alternative tariff schemes to determine whether switching would result in savings. Provides a clear financial verdict with monthly granularity. |
| **Primary Users** | Energy Managers, Finance, Procurement, Consultants |
| **Fuel Types** | Electricity only (tariff-structure-specific) |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Tariff Comparison — One & Only|Cape Town (8323)"
- **No date selectors visible** — uses the tariff's billing period automatically

### 2. AI Banner
- Purple gradient with "Download AI-Ready File (Beta)" CTA

### 3. Tariff Comparison Line Chart (★ Hero Visual)
- **Type:** Dual-line chart
- **Y-axis:** ZAR (1,000,000 – 2,000,000)
- **X-axis:** Monthly (Feb – Jan, 12-month period)
- **Series:**
  - 🔵 **Current tariff scheme** (blue line with markers)
  - 🔴 **Small Power Users 1** (red/coral line with markers)
- **Pattern:** Alternative scheme (red) sits consistently above current scheme (blue), except Jun–Aug where they converge (high-season tariff dynamics)

### 4. Action Cards (Right Sidebar — ★ Unique to this report)

| Card | Color | Content |
|------|-------|---------|
| **Analyse Tariff** | 🟠 Orange | "View Current Tariff Scheme Details" → links to tariff inspector |
| **Need Help?** | 🔵 Blue | "Request Assistance" → support/consultant contact |
| **Opportunity** | 🟢 Teal | "No savings available" (dynamic — would show savings if found) |

### 5. Cumulative Savings Comparison — Bar Chart
- **Type:** Bar chart (monthly bars, all negative = red)
- **Y-axis:** ZAR (-3,000,000 – 0)
- **X-axis:** Monthly
- **Pattern:** All bars point downward, growing cumulatively — confirming the alternative is worse every month
- **Legend:** Current tariff scheme (blue) | Small Power Users 1 (red/salmon)

### 6. Total Cost (ZAR) — Side-by-Side Summary
- **Type:** Simple bar comparison
- **Y-axis:** ZAR (0 – 20,000,000)
- **Bars:**
  - Blue: Current tariff scheme (~16.4M)
  - Red: Small Power Users 1 (~18.7M)
- **Legend:** Both scheme names

### 7. Tariff Comparison Table
- **Header:** Blue banner "Tariff Comparison" with XLSX, CSV, copy icons
- **Columns:** Month | Current tariff scheme (ZAR) | Small Power Users 1 (ZAR)
- **Row count:** 15 rows (12 months + Feb row at top + Total + Benefit verdict)

**Full data:**

| Month | Current Tariff (ZAR) | Small Power Users 1 (ZAR) |
|-------|---------------------|--------------------------|
| February 2025 | 1,086,211 | 1,356,634 |
| March 2025 | 1,180,168 | 1,541,456 |
| April 2025 | 1,168,548 | 1,530,971 |
| May 2025 | 1,231,746 | 1,595,519 |
| June 2025 | 1,707,222 | 1,526,574 |
| July 2025 | 1,815,751 | 1,703,806 |
| August 2025 | 1,688,447 | 1,629,558 |
| September 2025 | 1,182,318 | 1,413,822 |
| October 2025 | 1,261,992 | 1,497,997 |
| November 2025 | 1,322,356 | 1,592,205 |
| December 2025 | 1,405,604 | 1,694,604 |
| January 2025 | 1,381,685 | 1,647,607 |
| **Total (ZAR)** | **16,432,048** | **18,730,753** |
| **No apparent benefit** | — | **-2,298,705** (red text) |

**Key insight:** June–August the alternative is actually cheaper (winter tariff structure favors smaller users), but the annual total still shows a R2.3M penalty for switching.

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Tariff scheme selector | Dropdown (implied) | Available alternative tariffs | Small Power Users 1 |
| Analyse Tariff card | Navigation card | Opens tariff detail view | — |
| Need Help? card | Action card | Opens support contact | — |

---

## Downloads & Exports

| Export | Format | Trigger | Content |
|--------|--------|---------|---------|
| AI-Ready File | JSON | Banner button | Full comparison data |
| XLSX | Excel | Table header icon | Tariff comparison table |
| CSV | CSV | Table header icon | Same in CSV |
| Copy | Clipboard | Table header icon | Table data |

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| Tariff scheme comparison | ✅ Core feature | ❌ |
| Benefit/savings verdict | ✅ "No apparent benefit" / savings amount | ❌ |
| Cumulative savings chart | ✅ Shows compounding impact | ❌ |
| Action cards (Analyse/Help/Opportunity) | ✅ Three sidebar CTAs | ❌ |
| Total cost side-by-side | ✅ Clear annual visual | ❌ |
| No date picker | ✅ Uses tariff period automatically | All others have date pickers |
| Two-column simple table | ✅ Clean comparison format | Most have 6+ columns |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **Should we switch tariffs?** — No, the current scheme saves R2,298,705 annually.
2. **When is the alternative cheaper?** — June–August (high season), the alternative "Small Power Users 1" is slightly cheaper, but the annual total still favors the current scheme.
3. **What's the savings opportunity?** — The "Opportunity" card shows "No savings available" — dynamic; would highlight savings if an alternative were beneficial.
4. **How does cost trend monthly?** — The line chart reveals seasonal patterns and the consistent gap between schemes.
5. **Can I get a tariff analysis?** — "Analyse Tariff" card links to detailed tariff scheme inspector; "Need Help?" provides consultant access.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-comparison-chart-and-action-cards.png` | Tariff Comparison line chart (Current vs Small Power Users 1), three action cards (Analyse Tariff, Need Help?, Opportunity: No savings) |
| 02 | `02-cumulative-savings-and-total-cost.png` | Cumulative Savings bar chart (all negative/red), Total Cost side-by-side comparison, beginning of comparison table |
| 03 | `03-comparison-table-middle.png` | Monthly comparison table (March 2025 → January 2025) showing per-month costs for both schemes |
| 04 | `04-comparison-table-totals.png` | Table totals: Current 16,432,048 vs Alternative 18,730,753 + "No apparent benefit: -2,298,705" verdict |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Comparison Period: 12 months (February 2025 – January 2026)*
