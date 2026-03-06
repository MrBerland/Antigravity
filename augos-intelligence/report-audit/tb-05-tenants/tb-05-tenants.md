# TB-05: Tenants

> **Module:** Tenant Billing  
> **URL:** `live.augos.io/app/tenants`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Tenants page manages tenant entities across the entire portfolio. It tracks contact information, property/unit assignments, billing status, and outstanding balances. Tenants can be either Legal Persons (companies) or Natural Persons (individuals), with fields for registration numbers, VAT, and accounting system integration.

---

## Page Layout

### Header Bar
| Element | Description |
|---------|-------------|
| **Page Title** | "Tenants" with blue left-border accent |

### Section Banner
- Blue gradient banner with title "Tenants"
- Action buttons: Search (🔍), Export (📋), Add New (+), Reload (↻)
- Collapse/expand chevron (^)

### Tenants Table
| Column | Description |
|--------|-------------|
| **#** | Row number |
| **Tenant** | Tenant name + ID (e.g., "3 Star Barbershop (49064763)") |
| **Grouping** | Tenant grouping/category |
| **Primary Contact** | Contact person name |
| **Email** | Contact email address |
| **Phone number** | Contact phone (SA format: +27...) |
| **Property** | Linked property name |
| **Unit No.** | Linked unit reference |
| **Status** | Status badge: `Active` (teal/cyan) |
| **Current bill (ZAR)** | Current month billing amount |
| **Outstanding (ZAR)** | Overdue/unpaid balance |
| **⋮ (Actions)** | Context menu |

### Tenants Observed (15+ visible)
| # | Tenant | Property | Status | Current Bill | Outstanding |
|---|--------|----------|--------|-------------|-------------|
| 1 | 3 Star Barbershop (49064763) | Forlee Holdings\|She... | Active | 0 | 0 |
| 2 | African Cork (49062504) | — | Active | 0 | 0 |
| 3 | Alma Grove (49151988) | Bloempark\|Utility G... | Active | 0 | 0 |
| 4 | Anel Louw (49152018) | Bloempark\|Utility G... | Active | 0 | 0 |
| 7 | Benjamin Du Plessis (48382572) | Cape Town Market... | Active | 0 | 0 |
| 9 | Burger King (Tenant) (49941334) | Sun International\|Gr... | Active | 0 | 0 |

---

## Action Menu Options
| Action | Description |
|--------|-------------|
| **Edit** | Opens Add/Edit slide-out panel |
| **Lease History** | View tenant's lease history across units |
| **Contacts** | Manage additional contact details |
| **Delete** | Removes the tenant entity |

---

## Add / Edit Panel

### Entity Type Toggle
| Tab | Description |
|-----|-------------|
| **Legal person** (default, active) | Company/organization tenant |
| **Natural person** | Individual tenant |

### Info Card (Left)
- Blue gradient card with Augos logo
- "You are making changes to:" label
- **Tenant** heading  
- Tenant name + ID

### Edit Form (Right)
| Field | Type | Description |
|-------|------|-------------|
| **Tenant** | Text + autocomplete | Tenant name with clear/dropdown |
| **Tenant grouping** | Text | Category/grouping label |
| **Primary contact** | Contact selector | Select from existing contacts |
| **Email** | Text (readonly) | Contact email |
| **Phone number** | Text (readonly) | Contact phone |

### Additional Information Section
| Field | Type | Description |
|-------|------|-------------|
| **Registration No.** | Text | Company registration number |
| **Vat No.** | Text | VAT registration number |
| **Accounting Service Provider** | Text | Linked accounting system |
| **Accounting API Key** | Text | API key for accounting integration |

### Actions
- **CANCEL** / **SAVE** buttons

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| GET | `/api/tenants` | — |
| PUT | `/api/tenants/{id}` | `name`, `type`, `grouping`, `contact_id`, `registration_no`, `vat_no`, `accounting_provider`, `api_key` |
| POST | `/api/tenants` | Same as PUT |
| DELETE | `/api/tenants/{id}` | — |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-tenants-list.png` | Full tenants table with 15 entries showing status, billing, and property assignments |
| `02-edit-tenant.png` | Add/Edit panel showing Legal/Natural person toggle, contact fields, and Additional Information (Reg No, VAT, Accounting) |

---

## Key Insights

1. **Legal vs Natural person** — Dual entity type for corporate and individual tenants
2. **Accounting integration** — Built-in fields for Accounting Service Provider and API Key suggest automated invoice sync
3. **Financial visibility** — Current Bill and Outstanding columns provide at-a-glance debtor tracking
4. **Multi-property tenants** — A single tenant entity can span multiple properties/units
5. **All billable amounts showing 0** — Suggests billing run hasn't been finalized for this period
6. **Grouping field** — Allows categorization of tenants (e.g., by industry, franchise, etc.)
