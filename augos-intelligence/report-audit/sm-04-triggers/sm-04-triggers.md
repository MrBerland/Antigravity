# SM-04: Triggers

> **Module:** Sensing & Monitoring  
> **URL:** `live.augos.io/app/sensing-and-monitoring/triggers`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Triggers report provides a comprehensive alert management system. Users can define, edit, enable/disable, and monitor threshold-based alerts on any measurement parameter. With 342 configured triggers observed on this account, it's the backbone of the S&M alerting infrastructure.

---

## Page Layout

### Header Bar
| Element | Description |
|---------|-------------|
| **Page Title** | "Triggers" with blue left-border accent |

### Section Banner
- Blue gradient banner with title "Triggers"
- Action buttons: Search (🔍), Disable All (🚫), Add New (+), Reload (↻)
- Collapse/expand chevron (^)

### Trigger Table
| Column | Description | Sortable | Filterable |
|--------|-------------|----------|------------|
| **Description** | Trigger name + ID (e.g., "No voltage (48632815)") | ↓ | — |
| **Measurement Point** | Full path: Site\|Property\|Point (e.g., "Cape Grace Hotel\|Main Switch (5792)") | ↓ | — |
| **Status** | `Active` (blue badge) or `Inactive` | ↓ | ▼ |
| **Conditions** | Expanded inline showing Parameter, Condition, Value, Duration | — | ▼ |
| **Recurring** | Checkbox — whether the trigger re-fires on repeated breaches | — | — |
| **Recovered** | Checkbox — whether recovery notification is sent | — | — |

### Condition Details (Inline per Trigger)
| Field | Description |
|-------|-------------|
| **Parameter** | Monitored parameter (e.g., Voltage (3 phase), Peak Demand, Power Factor, Comms on device) |
| **Condition** | Logical operator + ID (e.g., "less than (48632816)", "greater than (49736759)", "equal to (49736806)") |
| **Value** | Threshold value with unit (e.g., "10 V", "1350 kVA", "0.94 PF", "Offline") |
| **Duration** | Time qualifier: `Instantaneous`, `For at least 1 minute`, `For at least 2 minutes`, `For at least 5 minutes` |

### Row Actions
| Icon | Action |
|------|--------|
| ✏ (Edit) | Opens the Add/Edit slide-out panel |
| 🗑 (Delete) | Removes the trigger |
| ⋮ (More) | Additional context menu options |

---

## Trigger Types Observed

| Type | Parameter | Condition | Example Value | Duration |
|------|-----------|-----------|--------------|----------|
| **No Voltage** | Voltage (3 phase) | less than | 10 V | Instantaneous |
| **Max Demand** | Peak Demand | greater than | 1350 kVA | For at least 1 minute |
| **Power Factor** | Power Factor | equal to | 0.94 PF | For at least 2 minutes |
| **Offline Meter** | Comms on device | equal to | Offline | For at least 5 minutes |
| **Voltage Spike Red** | V (a) | (not observed) | (not observed) | — |
| **Voltage Spike White** | V (b) | (not observed) | (not observed) | — |
| **Voltage Spike Blue** | V (c) | (not observed) | (not observed) | — |
| **PF Alert** | Power Factor | less than | 0.95 PF | For at least 10 minutes |
| **KVA Alert** | Peak Demand | greater than | (varies) | (varies) |

---

## Add / Edit Panel

The trigger edit flow uses a right-side slide-out panel:

### Left Section (Info Card)
- Blue gradient card showing:
  - "You are making changes to:" label
  - **Condition** heading
  - Trigger name + ID (e.g., "BFN - PF Alert (37560504)")
  - "Adding and Editing Information" warning: "By making additions or edits you will be changing points of measurement, site settings and service providers."

### Right Section (Edit Form)
| Field | Type | Description |
|-------|------|-------------|
| **Parameter** | Dropdown | Select monitored parameter (e.g., Power Factor) |
| **Condition** | Dropdown | Logical operator (less than, greater than, equal to) |
| **Value** | Text input | Threshold value with unit (e.g., "0.95 PF") |
| **Duration** | Radio group | `Instantaneous` · `Half-hour` · `For at least [N] [Minutes▼]` |

### Actions
- **CANCEL** — Discards changes
- **SAVE** — Commits the trigger configuration

---

## Functional Components

### 1. Search
- Filters the trigger list by description or measurement point name

### 2. Bulk Actions
- Disable All button (🚫) — toggles all triggers inactive
- Add New (+) — opens blank Add/Edit panel

### 3. Status Toggle
- Column filter to show Active/Inactive triggers
- Status badge color: Blue = Active

### 4. Duration Options
| Option | Description |
|--------|-------------|
| Instantaneous | Trigger fires immediately on breach |
| Half-hour | Trigger fires if breach persists for 30 minutes |
| For at least N minutes | Custom duration with configurable minute input |

---

## Data Points Observed

| Metric | Value |
|--------|-------|
| Total Triggers | 342 |
| Trigger Categories | No Voltage, Max Demand, Power Factor, Offline Meter, Voltage Spikes, PF Alerts, KVA Alerts |
| Sites Covered | Cape Grace Hotel, Clay Tile (Hercules Pilaar/Mega Plant), BFN (Countrybird), LTX, MBH (Countrybird/Nutri Feeds) |
| All Status | Active |

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| GET | `/api/sensing-monitoring/triggers` | — |
| PUT | `/api/sensing-monitoring/triggers/{id}` | `parameter`, `condition`, `value`, `duration`, `status` |
| POST | `/api/sensing-monitoring/triggers` | Same as PUT |
| DELETE | `/api/sensing-monitoring/triggers/{id}` | — |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-trigger-list.png` | Full trigger list showing 8 triggers with inline conditions |
| `02-edit-modal.png` | Add/Edit slide-out panel for PF Alert trigger |

---

## Key Insights

1. **Most complex CRUD page** in the platform — full create/read/update/delete with inline detail
2. **342 triggers** on this account suggest heavy production use
3. **Condition logic** supports less than, greater than, and equal to operators
4. **Duration flexibility** from Instantaneous to custom minute thresholds
5. **Phase-specific voltage monitoring** — Separate triggers for Red/White/Blue phases
6. **Consistent Add/Edit pattern** — Same slide-out panel pattern as Properties, Units, Tenants, Landlords
