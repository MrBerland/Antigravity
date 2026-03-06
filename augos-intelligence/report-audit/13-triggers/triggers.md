# Triggers

## Overview

| Property | Value |
|----------|-------|
| **URL** | `https://dev.live.augos.io/app/utilities-and-services/triggers?pointId=8323&productId=1` |
| **Purpose** | Alert configuration and management system. Displays all automated triggers across the organization, each with specific parameters, conditions, threshold values, and durations. Enables proactive monitoring of electrical anomalies, demand breaches, power factor drops, and device connectivity. |
| **Primary Users** | Energy Managers, Operations managers, System Administrators |
| **Fuel Types** | Electricity (primary — voltage, demand, power factor, comms) |
| **AI File** | ❌ No AI-Ready File option |
| **Scope** | ⚠️ **Organization-wide** — shows ALL triggers, not just the selected point ID |

---

## Page Layout (Top → Bottom)

### 1. Page Title
- **Title:** "Triggers" (standard format with blue left border)

### 2. Section Header Banner
- **Blue banner** with title "Triggers"
- **Toolbar icons (right side):**
  - 🔍 Search
  - ✕ Clear/filter (red)
  - 🔔 Notification bell
  - ⟳ Refresh
- **Collapse toggle** (^) at far right

### 3. Column Headers (Sortable)

| Column | Sortable | Filterable | Description |
|--------|----------|------------|-------------|
| **Description** | ✅ (↓ arrow) | — | Trigger name/description |
| **Measurement Point** | ✅ (↓ arrow) | — | Full point path with ID |
| **Status** | ✅ (↓ arrow) | ✅ (funnel icon) | Active / Inactive badge |
| **Conditions** | — | ✅ (funnel icon) | Expandable condition detail |
| **Recurring** | — | — | Checkbox |
| **Recovered** | — | — | Checkbox |

### 4. Trigger Rows (★ Rich Card Layout)

Each trigger is displayed as an expanded card-style row showing:

**Left Section:**
- **Description** — Truncated name (e.g., "No voltage (4863...", "Clay Tile Max Dem...")
- **Measurement Point** — Full hierarchical path (e.g., "Cape Grace Hotel|Main Switch (5792)")
- **Status Badge** — "Active" (blue pill badge)

**Right Section — Condition Details:**

| Field | Description | Examples |
|-------|-------------|----------|
| **Parameter** | What metric is monitored | Voltage (3 phase), Peak Demand, Power Factor, Comms on device, Demand (3 phase), V (a), V (b), V (c), Consumption |
| **Condition** | Comparison operator | less than, greater than, equal to |
| **Value** | Threshold value with unit | 10 V, 1350 kVA, 0.94 PF, Offline, 250 V, 1 kWh, 0.9 PF, 0.95 PF |
| **Duration** | Time the condition must persist | Instantaneous, For at least 1 minute, For at least 2 minutes, For at least 5 minutes, For at least 10 minutes, For at least 15 minutes, For at least 10080 minutes, Half-hour |

**Action Icons (per row):**
- ✏️ Edit — Modify trigger configuration
- 🗑️ Delete — Remove trigger
- ☐ Recurring — Enable recurring notifications
- ☐ Recovered — Notify when condition recovers
- ⋮ More options menu

### 5. Pagination Bar
- **Rows per page:** 25 (dropdown) 
- **Count:** "1–25 of 342"
- **Navigation:** < Previous | Next >

---

## Trigger Types Observed (From 342 Total)

### By Parameter Type

| Parameter | Count (visible) | Typical Condition | Typical Value | Typical Duration |
|-----------|----------------|-------------------|---------------|------------------|
| **Peak Demand** | 8+ | greater than / equal to | 500–2300 kVA | Instantaneous – 15 min |
| **Power Factor** | 6+ | less than / equal to | 0.9–0.95 PF | 2–10 minutes |
| **Voltage (3 phase)** | 1 | less than | 10 V | Instantaneous |
| **Voltage (per phase: a, b, c)** | 3 | greater than | 250 V | Instantaneous |
| **Comms on device** | 4+ | equal to | Offline | 5 min – 10080 min (7 days) |
| **Demand (3 phase)** | 1 | greater than | 1100 kVA | Instantaneous |
| **Consumption** | 1 | greater than | 1 kWh | Half-hour |

### By Site Observed

| Site | Measurement Point | Trigger Types |
|------|-------------------|---------------|
| Cape Grace Hotel | Main Switch (5792) | No voltage |
| Clay Tile | Hercules Pilaar (5868) | Max Demand, Power Factor, Offline monitoring |
| Countrybird Holdings | Nutri Feeds (multiple sub-points) | Peak Demand, PF, Voltage spikes |
| Deslee Mattex | Municipal Supply (Finishing, Weaving) | Peak Demand |
| FFS | Pietermaritzburg Main switch | Demand (3 phase) |
| John Thompson | Cape Town (7202) | Power Factor |
| Macsteel | VRN Cape Town | Peak Demand |
| MineBox | Zambia Immersion (7979) | Consumption |
| Myplas Proplas | Main switch (8116) | Comms offline, Peak Demand |

---

## Filters & Controls

| Control | Type | Options | Default |
|---------|------|---------|---------|
| Search | Icon button (🔍) | Text search across all columns | — |
| Status filter | Funnel icon on Status column | Active / Inactive | All |
| Conditions filter | Funnel icon on Conditions column | Filter by parameter type | All |
| Sort | Column header click | Description ↓, Measurement Point ↓, Status ↓ | Description ascending |
| Rows per page | Dropdown | 10, 25, 50, 100 | 25 |
| Page navigation | Arrows | < > | Page 1 |

---

## Downloads & Exports

| Export | Format | Notes |
|--------|--------|-------|
| None | — | No export functionality on this page |

**Note:** Triggers is the only report with NO export options — no XLSX, CSV, Copy, or AI-Ready file. This is a configuration/management interface, not a data report.

---

## Unique Features (vs Other Reports)

| Feature | This Report | Others |
|---------|-------------|--------|
| Organization-wide scope (not point-specific) | ✅ All triggers across all sites | ❌ Bound to selected pointId |
| CRUD operations (Edit/Delete) | ✅ Full create/read/update/delete | ❌ Read-only views |
| Alert/notification management | ✅ Configures automated alerts | ❌ No alert capabilities |
| Card-style expanded rows | ✅ Each row shows condition detail inline | ❌ Standard table rows |
| No data visualization | ✅ Configuration list only | ❌ All others have charts/tables |
| Recurring/Recovered checkboxes | ✅ Fine-grained notification control | ❌ |
| Duration-based thresholds | ✅ Time component to conditions | ❌ |
| Pagination (342 items) | ✅ Most data of any page by row count | Max ~24 rows in other tables |
| No AI file | ✅ | Most others have it |
| Search + column filters | ✅ Most advanced filtering interface | ❌ Other pages use date/fuel filters |

---

## API Calls (To Be Captured)

*Phase 2: Network tab inspection required — likely uses /triggers or /alarms endpoint*

---

## Key Insights This Report Provides

1. **What are we monitoring?** — Full visibility into every active trigger across the organization (342 total).
2. **What parameters are tracked?** — Peak Demand, Power Factor, Voltage, Device Connectivity (Comms), and Consumption.
3. **What are the thresholds?** — Specific numeric values for each trigger condition (e.g., Peak Demand > 1350 kVA).
4. **How quickly do we respond?** — Duration settings reveal alert urgency (Instantaneous vs 15 minutes vs 7 days).
5. **Which sites are most monitored?** — Sites like Clay Tile and Countrybird have multiple triggers, indicating higher monitoring priority.
6. **Are we notified on recovery?** — Recurring and Recovered checkboxes show notification strategy.
7. **Device health monitoring** — "Comms on device = Offline" triggers detect meter connectivity issues.

---

## Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01-header-and-first-triggers.png` | Page title, "Triggers" banner with search/notification icons, column headers (Description, Measurement Point, Status, Conditions, Recurring, Recovered), first 7 triggers including No voltage, Clay Tile Max Demand, Power Factor, and Offline monitors |
| 02 | `02-countrybird-triggers.png` | Countrybird Holdings triggers — BFN/LTX/MBH/VJK demand alerts, Power Factor alerts, Voltage Spike monitors (V(a), V(b), V(c) > 250V) |
| 03 | `03-varied-trigger-types.png` | Diverse trigger examples — Deslee Mattex demand, FFS 3-phase demand, John Thompson PF, Macsteel demand, MineBox consumption, Myplas comms offline + demand |
| 04 | `04-pagination-342-total.png` | Bottom of page showing pagination: "Rows per page: 25" dropdown, "1–25 of 342" count, navigation arrows |

---

*Audited: 23 Feb 2026*
*Scope: Organization-wide (all 342 triggers, not point-specific)*
*Note: This is a configuration/management tool, not a data visualization report*
