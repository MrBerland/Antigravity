# TB-06: Landlords

> **Module:** Tenant Billing  
> **URL:** `live.augos.io/app/landlord`  
> **Status:** ✅ Complete  
> **Audited:** 2026-02-25

---

## Overview

The Landlords page manages property owner entities. Each landlord is linked to one or more properties and contains contact, registration, and VAT information. This is the top of the billing hierarchy — Landlords own Properties, which contain Units, which are assigned to Tenants.

---

## Page Layout

### Header Bar
| Element | Description |
|---------|-------------|
| **Page Title** | "Landlords" with blue left-border accent |

### Section Banner
- Blue gradient banner with title "Landlords"
- Action buttons: Search (🔍), Export (📋), Add New (+), Reload (↻)
- Collapse/expand chevron (^)

### Landlords Table
| Column | Description |
|--------|-------------|
| **#** | Row number |
| **Description** | Landlord name + ID (e.g., "Cape Town Market (49022352)") |
| **Primary Contact** | Contact person name + ID |
| **Email** | Contact email address |
| **Status** | Status badge: `Active` (teal/cyan) |
| **# of properties** | Count of properties owned by this landlord |
| **⋮ (Actions)** | Context menu |

### Landlords Observed (9 total)

| # | Landlord | Primary Contact | Email | Status | Properties |
|---|----------|----------------|-------|--------|------------|
| 1 | Cape Town Market (49022352) | Ben Du Plessis (45850115) | power@ctmarket.co.za | Active | 1 |
| 2 | Forlee Investment Holdings (Pty) Ltd (49062349) | Caroline Coetzee (49061082) | caroline@forleeholdings.co.za | Active | 1 |
| 3 | Marriott\|Protea Hotels\|Sea Point Landlord (51302140) | Jeremiah Govender (4287) | jeremiah.govender@in2food.co.za | Active | 1 |
| 4 | Old Mutual (51283368) | Raymondoux Bowkers (44771602) | rbowkers2@oldmutual.com | Active | 1 |
| 5 | Sun International (49940998) | Jocelyn Roos (49940999) | jocelyn.roos@suninternational.com | Active | 1 |
| 6 | Tafelberg Trust (49151973) | Willie Grove (49151949) | willie@wilgrogroup.com | Active | 1 |
| 7 | Tafelberg Trust (49151987) | Willie Grove (49151949) | willie@wilgrogroup.com | Active | 1 |
| 8 | Urban Growth Developments (49062436) | Colin Young (3849) | colin.young@urbangrowth.co.za | Active | 1 |
| 9 | Work Spectrum (48611522) | Christopher Alan (48611523) | theonlychris24@gmail.com | Active | 1 |

### Pagination
- `Rows per page: 25 ▼`
- `1–9 of 9`

---

## Action Menu Options
| Action | Description |
|--------|-------------|
| **Edit** | Opens Add/Edit slide-out panel |
| **Contacts** | Manage additional contact details for the landlord |
| **View Properties** | Navigate to Properties filtered by this landlord |
| **Delete** | Removes the landlord entity |

---

## Add / Edit Panel

### Entity Type Toggle
| Tab | Description |
|-----|-------------|
| **Legal person** (default, active) | Company/organization landlord |
| **Natural person** | Individual property owner |

### Info Card (Left)
- Blue gradient card with Augos logo
- "You are making changes to:" label
- **Landlord** heading
- Landlord name

### Edit Form (Right)

#### Description Section
| Field | Type | Description |
|-------|------|-------------|
| **Name** | Text + autocomplete | Landlord entity name with clear/dropdown |
| **Landlord Grouping** | Text | Category/grouping label |

#### Contact Section
| Field | Type | Description |
|-------|------|-------------|
| **Name** | Contact selector | Primary contact with clear/dropdown |
| **Email** | Text (readonly) | Contact email (e.g., "power@ctmarket.co.za") |
| **Phone number** | Text | Contact phone number |

#### Additional Information Section
| Field | Type | Description |
|-------|------|-------------|
| **Registration No.** | Text | Company registration (e.g., "2002/011913/07") |
| **Vat No.** | Text | VAT number (e.g., "4370210322") |
| **Accounting Service Provider** | Text | Linked accounting system |

### Actions
- **CANCEL** / **SAVE** buttons

---

## Data Observations

### Landlord Data Quality
| Observation | Detail |
|-------------|--------|
| **Duplicate entries** | Tafelberg Trust appears twice (#6 and #7) with different IDs but same contact |
| **All 1 property each** | Every landlord has exactly 1 property — no multi-property landlords |
| **Real company data** | Registration and VAT numbers are populated for Cape Town Market |
| **Mixed formality** | Some landlords use pipe-separated hierarchical names (e.g., "Marriott\|Protea Hotels\|Sea Point Landlord") |

---

## API Endpoints (Inferred)

| Method | Endpoint | Parameters |
|--------|----------|------------|
| GET | `/api/landlord` | — |
| PUT | `/api/landlord/{id}` | `name`, `type`, `grouping`, `contact_id`, `registration_no`, `vat_no`, `accounting_provider` |
| POST | `/api/landlord` | Same as PUT |
| DELETE | `/api/landlord/{id}` | — |

---

## Screenshots

| File | Description |
|------|-------------|
| `01-landlords-list.png` | Full landlords table with 9 entries showing contacts, status, and property counts |
| `02-edit-landlord.png` | Add/Edit panel showing Cape Town Market with Registration No (2002/011913/07) and VAT No (4370210322) |

---

## Key Insights

1. **Top of billing hierarchy** — Landlord → Property → Unit → Tenant
2. **Legal/Natural person toggle** — Same pattern as Tenants
3. **Registration & VAT tracking** — Compliance with South African tax requirements
4. **Duplicate detection opportunity** — Tafelberg Trust (#6 & #7) appears to be duplicated
5. **All landlords have exactly 1 property** — Suggests 1:1 mapping in current configuration
6. **Accounting integration** — Same "Accounting Service Provider" field as Tenants
7. **Consistent UI pattern** — Identical slide-out panel structure across all TB admin pages
