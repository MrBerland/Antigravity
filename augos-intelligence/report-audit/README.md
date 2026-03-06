# Augos Report Intelligence Library

## Project Overview

Comprehensive functional audit of every report across **3 modules** of the Augos platform:
- **Utilities & Services** — 13 reports (energy analytics & cost management)
- **Sensing & Monitoring** — 4 reports (real-time sensor data & alerting)
- **Tenant Billing** — 6 reports (sub-metering, invoicing & entity management)

**Total: 23 reports audited** from `live.augos.io` (production environment).

### Purpose
This library serves as the single source of truth for:
- **Marketing & Content** — accurate feature descriptions, screenshots for collateral
- **Support** — quick-reference guides for customer questions
- **Engineering** — API endpoint documentation, data schemas
- **AI Agents** — structured specs for autonomous data collection, automated reporting, email digests

---

## Module 1: Utilities & Services

**Base URL:** `https://live.augos.io/app/utilities-and-services`  
**Sample Point ID:** `8323` (One & Only | Cape Town)

| # | Report | URL Slug | Status |
|---|--------|----------|--------|
| 01 | Dashboard | `/dashboard` | ✅ Complete |
| 02 | Technical Analysis | `/technical-analysis` | ✅ Complete |
| 03 | Consumption Breakdown | `/consumption-breakdown` | ✅ Complete |
| 04 | Cost Breakdown | `/cost-breakdown` | ✅ Complete |
| 05 | Cost Allocation | `/cost-allocation` | ✅ Complete |
| 06 | Bill Verification | `/bill-verification` | ✅ Complete |
| 07 | Power Factor & Demand | `/power-factor-and-demand` | ✅ Complete |
| 08 | Time of Use | `/time-of-use` | ✅ Complete |
| 09 | Tariff Comparison | `/tariff-comparison` | ✅ Complete |
| 10 | Load Curtailment | `/load-curtailment` | ✅ Complete |
| 11 | Charting | `/charting` | ✅ Complete |
| 12 | Data Download | `/data-download` | ✅ Complete |
| 13 | Triggers | `/triggers` | ✅ Complete |

## Module 2: Sensing & Monitoring

**Base URL:** `https://live.augos.io/app/sensing-and-monitoring`

| # | Report | URL Slug | Status |
|---|--------|----------|--------|
| SM-01 | Sensors (Dashboard) | `/status` | ✅ Complete |
| SM-02 | Charting | `/charting` | ✅ Complete |
| SM-03 | Data Download | `/data-download` | ✅ Complete |
| SM-04 | Triggers | `/triggers` | ✅ Complete |

## Module 3: Tenant Billing

**Base URL:** `https://live.augos.io/app`

| # | Report | URL Slug | Status |
|---|--------|----------|--------|
| TB-01 | Portfolio | `/portfolio` | ✅ Complete |
| TB-02 | Property Billing Run | `/property-billing-run` | ✅ Complete |
| TB-03 | Properties | `/properties` | ✅ Complete |
| TB-04 | Units | `/units` | ✅ Complete |
| TB-05 | Tenants | `/tenants` | ✅ Complete |
| TB-06 | Landlords | `/landlord` | ✅ Complete |

---

## Folder Structure

```
report-audit/
├── README.md                          # This file
│
├── ── Utilities & Services ──
├── 01-dashboard/         (4 screenshots, 1 doc)
├── 02-technical-analysis/ (5 screenshots, 1 doc)
├── 03-consumption-breakdown/ (4 screenshots, 1 doc)
├── 04-cost-breakdown/    (4 screenshots + 3 playwright, 1 doc)
├── 05-cost-allocation/   (4 screenshots, 1 doc)
├── 06-bill-verification/ (5 screenshots, 1 doc)
├── 07-power-factor-demand/ (4 screenshots, 1 doc)
├── 08-time-of-use/       (5 screenshots, 1 doc)
├── 09-tariff-comparison/ (4 screenshots, 1 doc)
├── 10-load-curtailment/  (4 screenshots, 1 doc)
├── 11-charting/          (3 screenshots + 3 playwright, 1 doc)
├── 12-data-download/     (2 screenshots, 1 doc)
├── 13-triggers/          (4 screenshots, 1 doc)
│
├── ── Sensing & Monitoring ──
├── sm-01-sensors/        (10 screenshots, 1 doc)
├── sm-02-charting/       (2 screenshots, 1 doc)
├── sm-03-data-download/  (2 screenshots, 1 doc)
├── sm-04-triggers/       (2 screenshots, 1 doc)
│
├── ── Tenant Billing ──
├── tb-01-portfolio/      (3 screenshots, 1 doc)
├── tb-02-property-billing-run/ (2 screenshots, 1 doc)
├── tb-03-properties/     (3 screenshots, 1 doc)
├── tb-04-units/          (2 screenshots, 1 doc)
├── tb-05-tenants/        (2 screenshots, 1 doc)
├── tb-06-landlords/      (2 screenshots, 1 doc)
│
├── ── Cross-Module Reference ──
├── api/
│   ├── api-reference.md               # ✅ Full API endpoint mapping
│   └── ai-file-schema.md              # ✅ AI-Ready file schema docs
└── scripts/
    └── audit-reports.js               # Playwright automation script
```

### Phase Status
- **Phase 1:** ✅ Complete — All 13 U&S reports audited (docs + screenshots)
- **Phase 2:** ✅ Complete — API endpoint mapping with verified response schemas
- **Phase 3:** ✅ Complete — AI-Ready file schema documentation (5 report types documented)
- **Phase 4:** ✅ Complete — Sensing & Monitoring module (4 reports, 16 screenshots)
- **Phase 5:** ✅ Complete — Tenant Billing module (6 reports, 14 screenshots)

---

## Audit Template (Per Report)

Each report markdown file follows this structure:

```markdown
# [Report Name]

## Overview
- **URL:** full URL with pointId
- **Purpose:** 1-2 sentence description
- **Primary Users:** who uses this and why
- **Fuel Types:** which fuels are supported

## Page Layout
- Numbered description of sections from top to bottom
- Include section names, positions, default states

## Components
### [Component Name]
- **Type:** chart / table / tree / filter / card / etc.
- **Data Points:** what metrics are displayed
- **Interactivity:** hover, click, filter, drill-down behaviors
- **Screenshot:** reference to screenshot file

## Filters & Controls
- Date selectors, fuel tabs, period toggles, view switches
- Default values and available options

## Downloads & Exports
- Export buttons, file formats
- AI-Ready JSON: URL pattern and payload structure

## API Calls
- Endpoints called on page load
- Endpoints called on interaction
- Request/response shapes

## Key Insights This Report Provides
- Business questions it answers
- Actionable outputs
```

---

## Naming Conventions

### Screenshots
- Format: `##-descriptor.png` (e.g., `01-full-page.png`, `02-hierarchy-tree.png`)
- Use lowercase with hyphens
- Number prefix ensures sort order matches page flow (top to bottom)

### Folders
- Format: `##-slug` matching the URL slug
- Two-digit prefix ensures consistent ordering

---

## Methodology

1. **Navigate** to report page with pointId=8323
2. **Wait** for full data load (all charts, tables, trees rendered)
3. **Capture** full-page screenshot at high resolution
4. **Scroll** through entire page, capturing each distinct component
5. **Document** every visible element, data point, and interaction
6. **Inspect** Network tab for API calls (endpoints, params, responses)
7. **Test** all interactive elements (filters, tabs, hover states, exports)
8. **Record** findings in structured markdown

---

*Project created: 23 Feb 2026*  
*Last updated: 23 Feb 2026*
