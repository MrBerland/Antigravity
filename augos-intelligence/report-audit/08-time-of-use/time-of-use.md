# Time of Use

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/time-of-use?pointId=8323&productId=1` |
| **Purpose** | Analyse electricity consumption patterns by Time-of-Use period (Standard, Peak, Off-peak), showing how energy usage distributes across hourly intervals, days of the week, and seasonal tariff periods. |
| **Primary Users** | Energy Managers, Operations, Finance, Procurement |
| **Fuel Types** | Electricity only (TOU is tariff-structure-specific) |
| **AI File** | ✅ Available — "Download AI-Ready File (Beta)" |

---

## Page Layout (Top → Bottom)

### 1. Header Bar
- **Page Title:** "Time of Use — One & Only|Cape Town (8323)"
- **Period quick-select pills:** Feb 26, Jan 26, Dec 25, Nov 25, Oct 25, **More**
- **Date range:** From 2026/02/01 00:00 / To 2026/02/28 23:59

### 2. AI Banner
- Purple gradient with "Download AI-Ready File (Beta)" CTA

### 3. Consumption vs Cost — Summary Section
- **Header:** Blue banner "Consumption vs Cost" with XLSX, CSV, copy icons, collapse toggle
- **Toggle:** Consumption | Cost (switches donut chart view)
- **Summary Table:**

| TOU Period | Color | Units (kWh) | % | Cost (ZAR) | % |
|------------|-------|-------------|---|-----------|---|
| Standard | 🔵 Blue | 171,821 | 40% | 372,989 | 40% |
| Peak | 🔴 Red | 65,558 | 15% | 218,939 | 23% |
| Off-peak | 🟢 Teal | 194,738 | 45% | 342,019 | 37% |
| **Total** | 🟢 Green | **432,118** | **100%** | **933,947** | **100%** |

- **Donut Chart:** Shows **432,118 kWh** / "Total Consumption" with Standard (40%), Peak (15%), Off-peak (45%) segments
- **Key insight:** Peak is only 15% of consumption but 23% of cost

### 4. Average Daily Energy Distribution — Heatmap (★ Distinctive)
- **Header:** Blue banner "Average Daily Energy Distribution" with XLSX, CSV, copy icons
- **Four tab views:**
  1. **Consumption Heatmap (kWh)** ← default
  2. Energy Cost Heatmap (ZAR)
  3. TOU Consumption Breakdown (kWh)
  4. TOU Cost Breakdown (ZAR)

- **Checkbox filters:** ☑ Standard, ☑ Peak, ☑ Off-peak (toggle visibility)
- **Structure:** 24 rows (01:00–24:00) × 7 columns (Monday–Sunday)
- **Color coding:** Green (low) → Yellow (medium) → Orange (high) → Red (very high)
- **Summary rows at bottom:**
  - Average Daily Consumption (kWh): Mon 16,144 | Tue 14,808 | ... | Sun 19,082
  - Average Cost per kWh (ZAR): Mon 2.29 | Tue 2.31 | ... | Sat 1.88 | Sun 1.79

**Heatmap data patterns:**
- Off-peak hours (01:00–05:00): ~480–690 kWh (green cells)
- Peak hours (07:00–09:00, weekdays): ~600–812 kWh (yellow-orange)
- Sunday consistently highest consumption across all hours (orange/red cells, up to 929 kWh)
- Saturday has lowest average cost per kWh (1.88 ZAR)

### 5. Energy Distribution Trend — Line Chart
- **Type:** Multi-line chart (7 lines, one per day of week)
- **Y-axis:** kWh (400–1,000)
- **X-axis:** Hourly intervals (00:00–24:00)
- **Toggle:** Consumption | Cost
- **Legend:** Monday through Sunday (each with unique color + markers)
- **Pattern:** All lines follow similar profile — low overnight (~450–600), ramp up at 06:00, plateau during business hours (~650–750), drop after 20:00
- **Sunday line clearly elevated** above all others

### 6. TOU Breakdowns — Historical Table
- **Header:** Blue banner "TOU Breakdowns" with XLSX, CSV, copy icons
- **Tab navigation:** **12 Month TOU Breakdown** | Daily TOU Breakdown
- **Columns:**

| Column | Description | Example |
|--------|-------------|---------|
| Period | Calendar month | Feb 26 |
| Season | Tariff season | Low / High |
| Standard Consumption | kWh in Standard period | 171,821 |
| % | Standard share | 39.8% |
| Peak Consumption | kWh in Peak period | 65,558 |
| % | Peak share | 15.2% |
| Off Peak Consumption | kWh in Off-peak period | 194,738 |
| % | Off-peak share | 45.1% |
| Total Consumption | Total kWh | 432,118 |
| Average Cost per kWh (ZAR) | Blended rate | 2.16 |

**Sample data (12 months):**

| Period | Season | Standard (kWh) | % | Peak (kWh) | % | Off-Peak (kWh) | % | Total (kWh) | Avg ZAR/kWh |
|--------|--------|---------------|---|-----------|---|---------------|---|------------|------------|
| Feb 26 | Low | 171,821 | 39.8% | 65,558 | 15.2% | 194,738 | 45.1% | 432,118 | 2.16 |
| Dec 25 | Low | 226,950 | 37.6% | 86,494 | 14.3% | 290,691 | 48.1% | 604,134 | 2.14 |
| Aug 25 | High | 222,508 | 38.3% | 85,068 | 14.6% | 273,316 | 47.1% | 580,892 | 2.74 |
| Jul 25 | High | 254,583 | 41.9% | 97,094 | 16.0% | 255,746 | 42.1% | 607,423 | 2.83 |
| Jun 25 | High | 192,627 | 33.0% | 88,522 | 15.2% | 302,711 | 51.8% | 583,859 | 2.59 |
| **Total** | — | **2,698,665** | **36.9%** | **1,098,799** | **15.0%** | **3,507,666** | **48.0%** | **7,305,130** | **2.15** |

**Key insight:** High season months (Jun–Aug) have avg cost 2.59–2.83 ZAR/kWh vs Low season 1.69–2.19 ZAR/kWh

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Period pills | Quick-select buttons | Feb 26, Jan 26, Dec 25, Nov 25, Oct 25, More | Feb 26 (current month) |
| Date From/To | DateTime pickers | Manual entry | Current month |
| Consumption / Cost toggle | Button pair | Consumption, Cost | Consumption |
| Heatmap tabs | Tab navigation | Consumption Heatmap, Energy Cost Heatmap, TOU Consumption, TOU Cost | Consumption Heatmap |
| TOU checkboxes | Checkboxes | Standard, Peak, Off-peak | All checked |
| TOU Breakdown tabs | Tab navigation | 12 Month TOU Breakdown, Daily TOU Breakdown | 12 Month |

---

## Downloads & Exports

| Export | Format | Trigger | Section |
|--------|--------|---------|---------|
| AI-Ready File | JSON | Banner button | Full report data |
| XLSX | Excel | Section header icon | Per-section data |
| CSV | CSV | Section header icon | Per-section data |
| Copy | Clipboard | Section header icon | Per-section data |

**Note:** Each of the three sections (Consumption vs Cost, Average Daily Distribution, TOU Breakdowns) has its own independent XLSX/CSV/copy export buttons.

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| TOU period breakdown (Standard/Peak/Off-peak) | ✅ Core feature | ❌ |
| Color-coded heatmap (24hr × 7 days) | ✅ Four heatmap views | ❌ |
| Day-of-week energy distribution trend | ✅ 7-line hourly chart | ❌ |
| Season column (High/Low) | ✅ In breakdown table | ❌ |
| Average cost per kWh tracking | ✅ Per-month and per-day | Cost Breakdown has total cost but not per-kWh avg |
| Period quick-select pills | ✅ Last 5 months + "More" | Most only have date pickers |
| Three independent export sections | ✅ Each section exports separately | Most have one export |
| Consumption/Cost toggle for donut | ✅ Switch donut view | ❌ |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required*

---

## Key Insights This Report Provides

1. **When is electricity most expensive?** — Peak period is 15% of usage but 23% of cost; High season months jump to 2.74–2.83 ZAR/kWh.
2. **What does the daily load profile look like?** — Heatmap instantly reveals patterns: ramp-up at 06:00, sustained load through business hours, wind-down after 20:00.
3. **Which day uses the most energy?** — Sunday consistently highest (19,082 kWh avg daily) at lowest cost/kWh (1.79). This is hotel-specific: leisure peak on weekends.
4. **What's the seasonal cost impact?** — High season (Jun–Aug) costs ~30% more per kWh than Low season.
5. **Where are load-shifting opportunities?** — Moving 10% of Peak consumption to Off-peak could save ~R22K/month based on the rate differential.
6. **What's the total annual consumption profile?** — 7,305,130 kWh annually at blended 2.15 ZAR/kWh.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-consumption-vs-cost-summary.png` | Consumption vs Cost summary table + donut chart (432,118 kWh), Standard/Peak/Off-peak split with percentage bars |
| 02 | `02-average-daily-heatmap.png` | Average Daily Energy Distribution heatmap (01:00–17:00 visible), 4 tab views, checkbox filters, color-coded cells (green→red) |
| 03 | `03-heatmap-bottom-and-trend.png` | Heatmap bottom rows (17:00–24:00), Average Daily totals/cost rows, Energy Distribution Trend 7-line hourly chart |
| 04 | `04-tou-breakdowns-table-top.png` | TOU Breakdowns table header, 12 Month/Daily tabs, Season (Low/High) column, Feb 26 → Aug 25 data |
| 05 | `05-tou-breakdowns-totals.png` | TOU Breakdowns Dec 25 → Feb 25 + Total row (7,305,130 kWh, avg 2.15 ZAR/kWh) |

---

*Audited: 23 Feb 2026*
*Site: One & Only | Cape Town (8323)*
*Date range: February 2026 (summary), 12 months (TOU Breakdowns)*
