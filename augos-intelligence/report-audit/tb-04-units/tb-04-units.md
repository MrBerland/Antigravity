# TB-04: Units

> **Module:** Tenant Billing  
> **URL:** `live.augos.io/app/units`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Units page manages individual rental/billing units within properties. Each unit represents a billable space (shop, office, apartment) linked to a property, landlord, tenant, and tariff scheme. This is the core configuration page for setting up the billing hierarchy.

---

## Page Layout

### Header Bar
| Element | Description |
|---------|-------------|
| **Page Title** | "Units" with blue left-border accent |

### Property Filter
| Element | Description |
|---------|-------------|
| **Label** | "Property" |
| **Dropdown** | "All" (default) — filters units by property |

### Section Banner
- Blue gradient banner with title "Units"
- Action buttons: Search (🔍), Add Calendar (📅+), Add New (+), Reload (↻)
- Collapse/expand chevron (^)

### Units Table
| Column | Description |
|--------|-------------|
| **#** | Row number |
| **Property** | Parent property name + ID |
| **Unit** | Unit name + ID (e.g., "Awerbuchs (47388968)") |
| **Landlord** | Landlord entity name |
| **Tenant** | Tenant name assigned to this unit |
| **Primary contract** | Contact person for the unit |
| **Email** | Contact email |
| **Lease start** | Lease commencement date (e.g., "2024/07/01 09:40") |
| **Lease expiry** | Lease end date (empty if ongoing) |
| **Tariff scheme** | Applied tariff (e.g., "CENTLEC (SOC) Ltd \| Commercial Pr...") |
| **⋮ (Actions)** | Context menu |

### Units Observed
All visible units belong to "Bloempark\|Utility Grid (47388947)" with Tafelberg Trust as landlord:
- Awerbuchs, Bier Huis, Copper Clover, Delta Express, Fluidra Waterlinx, Metsi, Moreson Pluimvee, Oxygenate, Park Wheels, PostNet, SAFARI 4x4, Splash Attack
- All use "CENTLEC (SOC) Ltd | Commercial Pr..." tariff scheme
- All leases start July 2024

---

## Action Menu Options
| Action | Description |
|--------|-------------|
| **Edit Unit** | Opens Add/Edit panel for unit details |
| **Edit Tenant and Lease** | Modify tenant assignment and lease terms |
| **View Lease History** | Audit trail of tenant changes |
| **Edit Tariff Scheme** | Change the billing rate applied to this unit |
| **View Tariff Scheme History** | Audit trail of tariff changes |
| **Delete** | Removes the unit |

---

## Add / Edit Panel

Consistent slide-out panel with:
- Blue info card showing unit being edited
- Form fields for unit description
- Warning about changes affecting billing configuration
- CANCEL / SAVE buttons

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| GET | `/api/units` | `property_id` (optional filter) |
| PUT | `/api/units/{id}` | `description`, `tenant_id`, `tariff_id`, `lease_start`, `lease_expiry` |
| POST | `/api/units` | Same as PUT |
| DELETE | `/api/units/{id}` | — |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-units-list.png` | Units table showing 12+ units for Bloempark with tenant/tariff details |
| `02-edit-unit.png` | Add/Edit slide-out panel for unit configuration |

---

## Key Insights

1. **Billing hierarchy core** — Units are the fundamental billable entity
2. **Tariff assignment** at unit level — Each unit can have its own tariff scheme
3. **Lease tracking** — Start and expiry dates enable automated tenant management
4. **Lease history** — Full audit trail for compliance and dispute resolution
5. **Tariff scheme history** — Track tariff changes per unit over time
6. **Property filtering** — Dropdown at top filters units by parent property
