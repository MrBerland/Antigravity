# Augos Intelligence Repository
### Private · Tim Stevens · augos-core-data

> **Access:** Private to Tim Stevens and authorised Antigravity instances only.  
> **Do not share** — contains proprietary platform intelligence, API schemas, and client data.

---

## What This Repository Contains

This repository is the consolidated knowledge base for the Augos platform, assembled from:
- Live crawl of `live.augos.io` (23 reports across 3 modules)
- HTML knowledge base pages built for the platform
- OEE visualisation experiments
- Full API reference with verified response schemas
- Augos platform site structure and report taxonomy

It is designed to be cloned on any Antigravity instance (MacBook, Mac mini, etc.) and kept in sync via Git.

---

## Structure

```
augos-intelligence/
│
├── README.md                     ← This file
│
├── api/                          ← API reference documentation
│   ├── api-reference.md          ← All 13 U&S endpoints, params, response schemas
│   └── ai-file-schema.md         ← AI-Ready file format documentation
│
├── knowledge-base/               ← 56 HTML knowledge base pages
│   ├── index.html                ← Master index / nav
│   ├── dashboard.html
│   ├── technical-analysis.html
│   ├── energy-intelligence.html
│   ├── oee-*.html                ← OEE knowledge articles (26 pages)
│   ├── data-governance.html
│   ├── the-power-of-people.html
│   ├── manufacturing-*.html
│   ├── case-study-coil-changes.html
│   ├── styles.css                ← Shared stylesheet
│   └── oee-knowledge.md         ← OEE knowledge base source
│
├── oee-visualisations/           ← 26 standalone OEE chart experiments
│   ├── oee-hierarchy-morph.html  ← Animated scroll-reveal Sankey (shipped)
│   ├── oee-sankey.html
│   ├── oee-waterfall-animated.html
│   ├── oee-matrix-explorer.html
│   └── [22 more variants]
│
├── report-audit/                 ← Full audit of live.augos.io
│   ├── README.md                 ← Audit overview (23 reports, 3 modules)
│   ├── energy-intelligence-audit.md
│   ├── 01-dashboard/
│   ├── 02-technical-analysis/
│   ├── 03-consumption-breakdown/
│   ├── 04-cost-breakdown/        ← Includes verified JSON response schema
│   ├── 05-cost-allocation/
│   ├── 06-bill-verification/
│   ├── 07-power-factor-demand/
│   ├── 08-time-of-use/
│   ├── 09-tariff-comparison/
│   ├── 10-load-curtailment/
│   ├── 11-charting/
│   ├── 12-data-download/
│   ├── 13-triggers/
│   ├── sm-01-sensors/            ← Sensing & Monitoring module
│   ├── sm-02-charting/
│   ├── sm-03-data-download/
│   ├── sm-04-triggers/
│   ├── tb-01-portfolio/          ← Tenant Billing module
│   ├── tb-02-property-billing-run/
│   ├── tb-03-properties/
│   ├── tb-04-units/
│   ├── tb-05-tenants/
│   └── tb-06-landlords/
│
└── tools/
    └── audit-reports.js          ← Playwright crawler (re-run anytime)
```

---

## API Quick Reference

**Base URL:** `https://live.augos.io`  
**Auth:** Cookie session (`token=...`) — see [Authentication](#authentication) below

### Utilities & Services Endpoints

| Report | Endpoint | Key Params |
|--------|----------|------------|
| Dashboard | `GET /api/v1/dashboard` | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| Technical Analysis | `GET /api/v1/technical-analysis` | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| Consumption Breakdown | `GET /api/v1/consumption-breakdown` | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| Cost Breakdown | `GET /api/v1/cost-breakdown` | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID`, `billing=0` |
| Cost Allocation | `GET /api/v1/cost-allocation` | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| Bill Verification | `GET /api/v1/bill-verification` | `pointID`, `startDateUTC`, `endDateUTC`, `productTypeID` |
| Power Factor & Demand | `GET /api/v1/power-factor-demand` | `pointID`, `startDateUTC`, `endDateUTC` |
| Time of Use | `GET /api/v1/electricity/time-of-use` | `pointID`, `startDateUTC`, `endDateUTC` |
| Tariff Comparison | `GET /api/v1/electricity/tariff-comparison` | `pointID` |
| Load Curtailment | `GET /api/v1/load-curtailment/get-load-curtailment` | `pointID`, `date`, `offset=-120` |
| Charting | `GET /api/v1/charting` | `pointID`, `startDateUTC`, `endDateUTC`, `parameterID`, `resolution` |
| Data Download | `GET /api/v1/data-download` | `pointID`, `startDateUTC`, `endDateUTC`, `format`, `phase` |
| Triggers | `GET /api/v1/triggers` | `page`, `pageSize` |

### Sample Point
- **Point ID:** `8323` — One & Only Cape Town (used for all audits)
- **Product Type ID:** `2` = Electricity

---

## Authentication

The Augos platform uses **cookie-based session authentication**.

### Method 1 — Reuse Browser Session (easiest)
The Playwright audit tool (`tools/audit-reports.js`) opens Chrome using your existing profile cookies. If you're already logged in to `live.augos.io` in Chrome, it just works.

```bash
cd augos-intelligence/tools
npm install playwright
node audit-reports.js
```

### Method 2 — Programmatic Login

```python
import requests

session = requests.Session()

# 1. Login
resp = session.post(
    "https://live.augos.io/api/auth/login",
    json={"email": "tim@augos.io", "password": "YOUR_PASSWORD"}
)
# Session cookie is now set automatically in the session object

# 2. Query any endpoint
data = session.get(
    "https://live.augos.io/api/v1/cost-breakdown",
    params={
        "pointID": 8323,
        "startDateUTC": "2026-01-01",
        "endDateUTC": "2026-01-31",
        "productTypeID": 2,
        "billing": 0
    }
).json()
```

### Method 3 — Cookie String (from DevTools)
1. Open `live.augos.io` in Chrome, log in
2. Open DevTools → Network → any API request → Headers → `cookie: token=xxx`
3. Copy the `token=` value

```python
headers = {"Cookie": "token=YOUR_TOKEN_HERE"}
resp = requests.get("https://live.augos.io/api/v1/dashboard?pointID=8323...", headers=headers)
```

> **Note:** Session tokens expire. Re-login or re-copy cookie if you get 401 responses.

---

## Site Structure

### Module 1 — Utilities & Services
**URL:** `https://live.augos.io/app/utilities-and-services/{slug}?pointId={id}&productId=1`

### Module 2 — Sensing & Monitoring  
**URL:** `https://live.augos.io/app/sensing-and-monitoring/{slug}?pointId={id}`

### Module 3 — Tenant Billing
**URL:** `https://live.augos.io/app/{slug}`

---

## For Antigravity Instances

When an Antigravity instance needs platform knowledge, it should:

1. Read `api/api-reference.md` for endpoint specifications
2. Read the relevant `report-audit/NN-report-name/` folder for full report context
3. Open `knowledge-base/index.html` for the full KB browser
4. Reference `oee-visualisations/` for chart component options

---

*Last updated: 6 March 2026*  
*Captured from: `live.augos.io` · Point 8323 (One & Only Cape Town)*  
*Method: Playwright DOM extraction + Network monitoring*
