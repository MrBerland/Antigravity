# TB-03: Properties

> **Module:** Tenant Billing  
> **URL:** `live.augos.io/app/properties`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Properties report is an admin/configuration page for managing physical property assets within the Tenant Billing system. It lists all properties with their landlord, contacts, location, and linked entity counts (Units, Devices, Measurement Points).

---

## Page Layout

### Header Bar
| Element | Description |
|---------|-------------|
| **Page Title** | "Properties" with blue left-border accent |

### Section Banner
- Blue gradient banner with house icon (🏠) and title "Properties"
- Action buttons: Search (🔍), Filter (≡+), Add New (+), Reload (↻)
- Collapse/expand chevron (^)

### Properties Table
| Column | Description |
|--------|-------------|
| **#** | Row number (1-indexed) |
| **Description** | Property name + ID (e.g., "Bloempark\|Utility Grid (47388947)") |
| **Landlord** | Landlord entity name (e.g., "Tafelberg Trust", "Cape Town Market") |
| **Primary contact** | Contact person name |
| **Email** | Contact email address |
| **Location** | Physical address with map pin (📍) icon |
| **# of Units** | Count of billing units in the property |
| **# of Devices** | Count of smart meters/devices installed |
| **# of Measurement Points** | Count of configured measurement points |
| **⋮ (Actions)** | Context menu for property management |

### Properties Observed (10 total)

| # | Property | Landlord | Units | Devices | Measurement Points |
|---|----------|----------|-------|---------|-------------------|
| 1 | Bloempark\|Utility Grid (47388947) | Tafelberg Trust | 15 | 1 | 1 |
| 2 | Cape Town Market Site Total (36040590) | Cape Town Market | 2 | 59 | 85 |
| 3 | Forlee Holdings\|Fiveways Centre\|Mains (49061073) | Forlee Investment Holdings | 13 | 15 | 15 |
| 4 | Forlee Holdings\|Sherwood Centre\|Mains (49061068) | Forlee Investment Holdings | 13 | 14 | 14 |
| 5 | Marriott\|Protea Hotels\|Sea Point (14426) | Marriott\|Protea Hotels\|Sea Poi... | 1 | 10 | 13 |
| 6 | Old Mutual\|Pinelands HO (51292506) | Old Mutual | 1 | 7 | 10 |
| 7 | Sun International\|Grand West (14546) | Sun International | 30 | 137 | 138 |
| 8 | The Crest Estate Office Park (17190) | — | 2 | 12 | 54 |
| 9 | Urban Growth\|Park (Paarl) (10457) | Urban Growth Developments | 11 | 26 | 31 |
| 10 | Work Spectrum (17635) | Work Spectrum | 10 | 10 | 11 |

### Pagination
- `Rows per page: 25 ▼`
- `1–10 of 10`

---

## Action Menu Options

When clicking the ⋮ (three-dot) icon for a property:
| Action | Description |
|--------|-------------|
| **Edit Property** | Opens Add/Edit slide-out panel |
| **Landlord & Ownership** | Configure legal ownership |
| **Ownership History** | Audit log of previous owners |
| **View Units** | Navigate to Units filtered by property |
| **View Devices** | Navigate to Devices filtered by property |
| **View Measurement Points** | Navigate to Measurement Points filtered by property |
| **Tariff Scheme** | Configure billing rates and logic |

---

## Add / Edit Panel

Right-side slide-out panel (consistent pattern across all TB admin pages):

### Left Section (Info Card)
- Blue gradient card with Augos logo
- "You are making changes to:" label
- **Property** heading
- Property name + ID

### Right Section (Edit Form)
- Property description input field
- Warning: "Adding and Editing Information — By making additions or edits you will be changing points of measurement, site settings and service providers."
- **CANCEL** and **SAVE** buttons

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| GET | `/api/properties` | — |
| PUT | `/api/properties/{id}` | `description`, `landlord_id` |
| POST | `/api/properties` | `description`, `landlord_id`, `location` |
| DELETE | `/api/properties/{id}` | — |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-properties-list.png` | Full properties table with 10 properties and entity counts |
| `02-action-menu.png` | Expanded action menu showing Edit, Landlord, History, View options |
| `03-edit-property.png` | Add/Edit slide-out panel for property editing |

---

## Key Insights

1. **Configuration page** — Not a report, but an admin tool for managing billing structure
2. **Entity relationships** — Properties link to Landlords, Units, Devices, and Measurement Points
3. **Scale indicator** — Sun International has 30 units and 137 devices (largest property)
4. **Tariff Scheme management** — Each property has configurable billing logic
5. **Ownership tracking** — Full audit trail of property ownership changes
6. **Consistent CRUD pattern** — Same Add/Edit slide-out as Triggers, Units, Tenants, Landlords
