# Bill Verification

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/bill-verification?pointId=8323&productId=1` |
| **Purpose** | Compare utility bills received from the municipality against Augos-calculated estimates. Identify overcharges, undercharges, and missing billing periods. |
| **Primary Users** | Finance Teams, Procurement, Energy Managers |
| **Fuel Types** | Electricity, Water, Fuel, Gas |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Bill Verification — One & Only|Cape Town (8323)"
- **Site name link:** Editable/searchable field showing "One & Only|Cape Town (8323)"

### 2. Fuel Selector
- Toggle buttons: **Electricity** (default), Water, Fuel, Gas

### 3. AI Banner
- Purple gradient with "Download AI-Ready File (Beta)" CTA
- **Note:** No date range controls — this report spans all historical data

### 4. Bill Verification Records — Historic Trend Chart
- **Type:** Combo chart (bar + line)
- **Left Y-axis:** ZAR (0–1.2M range)
- **Right Y-axis:** Variance % (-80% to 160%)
- **X-axis:** Monthly periods
- **Series:**
  - 🟠 **Estimate** (orange bars) — Augos-calculated cost based on measured data + tariff
  - 🔵 **Utility bill** (blue bars) — Actual invoice amount from municipality
  - 🔴 **Variance** (red line with data points) — % difference between bill and estimate
- **Red ✕ markers:** On variance line where data is flagged as problematic

### 5. Action Cards (Right Sidebar — ★ Distinctive)
Three vertically stacked action cards:

| Card | Color | Title | Description | CTA |
|------|-------|-------|-------------|-----|
| 1 | 🔴 Red/coral | "Action Required!" | "Bill Verification Overdue" — "Verify your billing" | → Arrow |
| 2 | 🟠 Orange/gold | "Tariff Opportunity" | "Analyse Tariff" with trend icon | → Arrow |
| 3 | 🔵 Blue | "Bill Verification" | "Add bill Verification" with document icon | → Arrow |

### 6. Report Comparison Table
- **Header:** Blue banner "Report Comparison" with XLSX, CSV, copy (📋), refresh (↻) buttons, collapse toggle
- **Structure:** Three column groups:

| Group | Columns |
|-------|---------|
| **Consumption (kWh)** | Bill, Estimate, Variance (%) |
| **Demand (kVa)** | Bill, Estimate, Variance (%) |
| **Cost (ZAR)** | Bill, Estimate, Variance (%) |

- **First column:** Period (date range, e.g., "2021/01/01 to 2021/01/31")
- **Status indicators:**
  - ✅ Green check — Bill verified, variance acceptable (e.g., -0.5%)
  - ❌ Red cross — Bill unverified or variance too high (e.g., 100%)
  - ⋮ Kebab menu — Per-row actions
- **Gap rows:** Orange text "Period between [date] to [date] has not been verified" with "ADD PERIOD" button

**Sample data:**

| Period | Bill (kWh) | Estimate (kWh) | Var % | Bill (kVa) | Estimate (kVa) | Var % | Bill (ZAR) | Estimate (ZAR) | Var % | Status |
|--------|-----------|----------------|-------|-----------|----------------|-------|-----------|----------------|-------|--------|
| 2021/01/01–01/31 | 586,224 | 584,980.25 | -0.2% | 1,153.25 | 1,143.03 | -0.9% | 926,181.69 | 921,995.89 | -0.5% | ✅ |
| 2021/09/01–09/30 | 0 | 317,120.09 | 100% | 0 | 1,020.60 | 100% | 0 | 698,614.12 | 100% | ❌ |
| 2020/11/23–12/31 | 736,608 | 0 | 100% | 1,164.48 | 0 | 100% | 1,082,291.80 | 332,573.89 | -69.3% | ❌ |

### 7. Pagination
- **Controls:** "Rows per page: 25" dropdown, "1–18 of 18" counter, < > navigation
- **Note:** Shows 18 total periods spanning from 2019 to present

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Fuel Type | Toggle buttons | Electricity, Water, Fuel, Gas | Electricity |
| Rows per page | Dropdown | 10, 25, 50, 100 | 25 |

**Note:** No date range selector — the report always shows all available historical periods.

---

## Downloads & Exports

| Export | Format | Trigger | Content |
|--------|--------|---------|---------|
| AI-Ready File | JSON | Banner button | Full bill verification data |
| XLSX | Excel | Report Comparison header XLSX icon | Comparison table data |
| CSV | CSV | Report Comparison header CSV icon | Same in CSV format |
| Copy | Clipboard | Report Comparison header copy icon | Table data |

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| Bill vs Estimate comparison | ✅ Three-way (Consumption, Demand, Cost) | ❌ |
| Variance % with visual flags | ✅ ✅/❌ status per period | ❌ |
| Action cards sidebar | ✅ Three contextual CTAs | ❌ |
| "ADD PERIOD" inline prompts | ✅ For missing periods | ❌ |
| Historic trend combo chart | ✅ Bar + line with dual Y-axis | ❌ |
| No date range filter | ✅ Shows all history | ❌ (all others have date filters) |
| Paginated table | ✅ | ❌ (most others scroll) |
| Tariff opportunity link | ✅ Direct path to tariff analysis | ❌ |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **Are we being overcharged?** — Variance % reveals if the utility bill differs from the measured estimate.
2. **Are bills being submitted consistently?** — Gap rows with "ADD PERIOD" highlight missing verification periods.
3. **What's the long-term billing trend?** — Historic chart shows cost estimates and actual bills over years.
4. **When were bills last verified?** — "Bill Verification Overdue" action card immediately flags stale verification.
5. **Is there a tariff optimisation opportunity?** — "Analyse Tariff" card directs users to tariff comparison.
6. **What's the data quality?** — Periods with 100% variance (bill=0 or estimate=0) indicate data gaps.

---

## Screenshots

### One & Only | Cape Town (8323) — With Historical Bills
| # | File | Description |
|---|------|-------------|
| 01 | `01-trend-chart-and-action-cards.png` | Historic Trend combo chart (Estimate vs Utility bill bars, Variance line), three action cards (Overdue, Tariff, Add Bill) |
| 02 | `02-report-comparison-table.png` | Report Comparison table with Consumption/Demand/Cost columns, ✅/❌ status, "ADD PERIOD" gap rows |
| 03 | `03-historical-records-and-pagination.png` | Historical records from 2019 with ADD PERIOD gaps, pagination controls (1–18 of 18) |

### Pioneer Foods|Essential Foods|Mills|Malmesbury|Municipal Supply (48348717) — Empty State
| # | File | Description |
|---|------|-------------|
| 04 | `04-pioneer-foods-empty-state.png` | Empty state — "There are no bills yet" with empty chart and "Add bill Verification" card only |
| 05 | `05-fuel-consultant-modal.png` | Fuel tab triggers consultation modal: "Would you like a consultant to contact you regarding Fuel measurement?" |

**Note:** Pioneer Foods (48348717) has Electricity, Fuel, Gas, and Water tabs but no bills have been submitted for any fuel type. The Fuel/Water tabs trigger a consultant contact modal, indicating measurement isn't active for those fuel types.

---

*Audited: 23 Feb 2026*
*Sites: One & Only | Cape Town (8323), Pioneer Foods (48348717)*
*Data range: All historical periods*
