# Augos Report Intelligence Library

## Project Overview

Comprehensive functional audit of every report in **Utilities & Services** for the Augos platform.  
All data captured from **One & Only | Cape Town (Point ID: 8323)**.

### Purpose
This library serves as the single source of truth for:
- **Marketing & Content** — accurate feature descriptions, screenshots for collateral
- **Support** — quick-reference guides for customer questions
- **Engineering** — API endpoint documentation, data schemas
- **AI Agents** — structured specs for autonomous data collection, automated reporting, email digests

---

## Reports In Scope

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

**Base URL:** `https://dev.live.augos.io/app/utilities-and-services`  
**Point ID:** `8323` (One & Only | Cape Town)

---

## Folder Structure

```
report-audit/
├── README.md                          # This file
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
├── api/
│   ├── api-reference.md               # ✅ Full API endpoint mapping (Phase 2)
│   └── ai-file-schema.md              # ✅ AI-Ready file schema docs (Phase 3)
└── scripts/
    └── audit-reports.js               # Playwright automation script
```

### Phase Status
- **Phase 1:** ✅ Complete — All 13 reports audited (docs + screenshots)
- **Phase 2:** ✅ Complete — API endpoint mapping with verified response schemas
- **Phase 3:** ✅ Complete — AI-Ready file schema documentation (5 report types documented)

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
