# Power Factor & Demand

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/power-factor-and-demand?pointId=8323&productId=1` |
| **Purpose** | Analyse power factor performance, peak demand, and the financial impact (actual & potential losses) of poor power factor over time. Identify whether power factor correction equipment is needed. |
| **Primary Users** | Energy Managers, Electrical Engineers, Facility Operations |
| **Fuel Types** | Electricity only (power factor is an electrical concept) |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Power Factor & Demand — One & Only|Cape Town (8323)"
- **Date range:** From 2024/03/01 to 2026/02/28 (24-month default)

### 2. AI Banner
- Purple gradient with "Download AI-Ready File (Beta)" CTA

### 3. Peak Demand & Power Factor — 24 Month Trend Chart (★ Hero Chart)
- **Type:** Combo chart (stacked bars + multiple lines)
- **Left Y-axis:** kW/kVA (0–1,500)
- **Right Y-axis:** Power Factor (0.88–1.00)
- **X-axis:** Monthly (Mar 24 → Feb 26)
- **Bar series:**
  - 🟢 **Power factor lagging (+)** — cyan/teal bars (reactive power absorbed)
  - 🟠 **Power factor leading (-)** — orange bars (reactive power generated)
- **Line series:**
  - 🔵 **Power at Peak** (blue line)
  - 🔴 **Peak Demand** (red/coral line)
  - 🟣 **Reactive Power** (pink/magenta line)

### 4. Summary KPI Cards (★ Distinctive — 4 cards)

| Card | Period | Value | Sub-metric |
|------|--------|-------|-----------|
| **Actual Loss (ZAR)** | 2024/03/01 – 2026/02/28 | **62,201** | This Month: 3,721 (with ← trend arrow) |
| **Potential Loss (ZAR)** | 2024/03/01 – 2026/02/28 | **64,154** | This Month: 1 (with ← trend arrow) |
| **Power Factor Performance** | PF at Peak in last 30 days | **0.96** | Max Demand: 1,233.53 kVA (with ← trend arrow) |
| **System Status** | Based on PF at Peak in last 30 days | **"Under Capacity"** | 329.42 kVAr — "System Requires Attention" (coral/red card with → arrow) |

### 5. Main Point/s Contribution Chart
- **Type:** Stacked bar chart (24-month)
- **Y-axis:** ZAR (0–8,000)
- **X-axis:** Monthly
- **Series:** Main Switch 1 (🟠 orange) + Main Switch 2 (🟢 teal)
- **Dropdown filter:** "Actual Cost" (suggests other views: Potential Cost, etc.)

### 6. Total Value (ZAR) Donut Chart
- **Type:** Donut chart
- **Centre text:** **66,231** — "Site Total (ZAR)"
- **Over 24 months** subtitle
- **Segments:** Match the Main Switch colors

### 7. Performance Table
- **Header:** Blue banner "Performance" with XLSX, CSV, copy icons
- **Tab navigation:** **Summary** | Detail Actual | Detail Potential
- **Columns:**

| Column | Description | Example |
|--------|-------------|---------|
| ⊕ | Expand row (drill into Main Switch 1 & 2) | + icon |
| Month | Calendar month | Feb 26 |
| Date & Time of Peak | Exact timestamp of max demand event | 2026/02/11 10:30 |
| Peak Demand (kVA) | Maximum apparent power | 1,131.44 |
| Power at Peak (kW) | Active power at that moment | 1,082.43 |
| Power Factor | kW/kVA ratio at peak | 0.96 |
| Actual Loss (ZAR) | Financial loss from current power factor | 3,720.72 |
| Potential Loss (ZAR) | What losses would be if PF corrected to target | 3,978.35 |

**Sample data (24 months):**

| Month | Date & Time of Peak | Peak Demand (kVA) | Power at Peak (kW) | PF | Actual Loss (ZAR) | Potential Loss (ZAR) |
|-------|--------------------|--------------------|---------------------|-----|-------------------|---------------------|
| Feb 26 | 2026/02/11 10:30 | 1,131.44 | 1,082.43 | 0.96 | 3,720.72 | 3,978.35 |
| Jan 26 | 2026/01/02 15:00 | 1,233.53 | 1,186.64 | 0.96 | 3,558.79 | 4,025.72 |
| Dec 25 | 2025/12/29 16:00 | 1,190.37 | 1,153.70 | 0.97 | 2,783.04 | 2,930.03 |
| Nov 25 | 2025/11/25 16:00 | 1,036.32 | 1,013.75 | 0.98 | 1,712.52 | 1,625.57 |
| Oct 25 | 2025/10/27 10:00 | 919.43 | 907.36 | 0.99 | 916.53 | 801.08 |
| Mar 24 | 2024/03/19 16:30 | 1,017.73 | 984.12 | 0.97 | 5,190.57 | 3,979.67 |
| **Total** | — | — | — | — | **62,201.13** | **64,153.78** |

### 8. Expandable Row Detail
Each month row can be expanded (+ button) to show per-switch breakdown (Main Switch 1, Main Switch 2).

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Date From/To | DateTime pickers | Manual entry | 24-month window |
| Contribution chart dropdown | Select | Actual Cost, Potential Cost, etc. | Actual Cost |
| Performance tab | Tab navigation | Summary, Detail Actual, Detail Potential | Summary |
| Row expand/collapse | ⊕ buttons | Per row | Collapsed |

---

## Downloads & Exports

| Export | Format | Trigger | Content |
|--------|--------|---------|---------|
| AI-Ready File | JSON | Banner button | Full power factor data |
| XLSX | Excel | Performance header XLSX icon | Performance table data |
| CSV | CSV | Performance header CSV icon | Same in CSV |
| Copy | Clipboard | Performance header copy icon | Table data |

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| Power factor analysis | ✅ Core feature | ❌ |
| Reactive power tracking | ✅ kVAr values and bars | ❌ |
| System health status card | ✅ "Under Capacity" / "Requires Attention" | ❌ |
| Actual vs Potential loss comparison | ✅ Shows savings potential | ❌ |
| Per-switch contribution | ✅ Main Switch 1 & 2 breakdown | ❌ |
| Date & time of peak event | ✅ Exact timestamp per month | ❌ |
| 24-month default range | ✅ Long-term view by default | Most default to 1 month |
| Three tab views | ✅ Summary/Detail Actual/Detail Potential | ❌ |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **Is the power factor healthy?** — 0.96 at peak currently; it was 0.99 in mid-2025, so degradation is occurring.
2. **How much money is being lost?** — R62,201 in actual losses over 24 months; R3,721 this month alone.
3. **Is correction equipment needed?** — "System Requires Attention" + "Under Capacity" (329.42 kVAr) suggests yes.
4. **Which incoming supplies are worse?** — Main Switch 1 vs 2 contribution chart isolates the source.
5. **When do peaks happen?** — Exact timestamps help identify patterns (e.g., winter mornings, summer afternoons).
6. **What would savings look like?** — Potential Loss column shows theoretical costs if PF were corrected.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-peak-demand-trend-chart.png` | 24-month Peak Demand & Power Factor combo chart — bars (lagging/leading PF), lines (Power at Peak, Peak Demand, Reactive Power) |
| 02 | `02-kpi-cards-and-contribution-charts.png` | Four KPI cards (Actual Loss 62,201, Potential Loss 64,154, PF 0.96, System Status "Under Capacity"), Main Point/s Contribution 24-month bar chart, Total Value donut (66,231 ZAR) |
| 03 | `03-performance-table-top.png` | Performance table (Summary tab) with XLSX/CSV export, showing Feb 26 → Apr 25 with expandable rows |
| 04 | `04-performance-table-totals.png` | Table bottom showing Feb 25 → Mar 24 and Total row (Actual Loss: 62,201.13 / Potential Loss: 64,153.78) |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Date range: 24 months (March 2024 – February 2026)*
