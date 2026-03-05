---
description: Download company logos from the web and embed them as base64 data URIs in HTML files
---

# Logo Extraction & Embedding Workflow

// turbo-all

This workflow downloads brand logos from official sources, converts them to base64 data URIs, and embeds them inline in HTML proposal files. This makes proposals fully self-contained with no external dependencies.

## Brand Registry

All client logos are catalogued in `/Users/timstevens/Antigravity/logos/brand_registry.json` with:
- **name** — Brand display name
- **sector** — Industry sector (Healthcare, Financial Services, FMCG & Manufacturing, Retail & Grocery, Hospitality, Energy & Petroleum, Automotive)
- **sub_sector** — More specific classification (e.g. "Food Manufacturing", "Beverage Manufacturing")
- **tags** — Searchable tags for flexible queries (e.g. "food manufacturer", "multinational", "JSE listed")
- **logo_file** — Filename in the `logos/` directory (null if text fallback is used)
- **logo_colors** — Brand primary/secondary colors for fallback SVGs

### Query Examples
- **"hospitality brands"** → filter by `sector == 'Hospitality'`
- **"manufacturers"** → filter by `'manufacturer' in tags`
- **"food manufacturers"** → filter by `'food manufacturer' in tags`
- **"South African companies"** → filter by `country == 'South Africa'`
- **"JSE listed"** → filter by `'JSE listed' in tags`
- **"retail brands"** → filter by `sector == 'Retail & Grocery'`

When the user asks for logos by category, read `brand_registry.json`, filter by the requested criteria, and use the corresponding logo files.

## Steps

1. Read the brand registry to determine which logos are needed:
```bash
cat /Users/timstevens/Antigravity/logos/brand_registry.json | python3 -m json.tool
```

2. For new brands not yet in the registry, download logos using curl with a browser user-agent:
```bash
cd /Users/timstevens/Antigravity/logos && curl -sL -A 'Mozilla/5.0' -o <filename> "<url>"
```

3. Verify downloaded files are valid images/SVGs:
```bash
cd /Users/timstevens/Antigravity/logos && file *.svg *.png 2>/dev/null
```

4. For SVGs with white fills (designed for dark backgrounds), convert to dark fills:
```bash
sed 's/fill="#fff"/fill="#1a1a2e"/g' input.svg > output_dark.svg
```

5. For brands where direct download fails, create typographic SVG logos using brand colors from the registry.

6. Update the brand registry with new entries (sector, sub_sector, tags, logo_file, etc.)

7. Run the Python embedding script to convert selected logos to base64 data URIs and inject into the target HTML:
```bash
python3 /Users/timstevens/Antigravity/create_logo_bar.py
```

8. Verify the result by opening the HTML in the browser and taking a screenshot.

## Adding New Brands

When adding a new brand to the registry:
1. Search for the brand's official website
2. Navigate to the site and extract the header logo URL
3. Download it to `/Users/timstevens/Antigravity/logos/`
4. Add a new entry to `brand_registry.json` with full classification
5. Prefer SVG > PNG > JPG for quality
6. Always include: sector, sub_sector, tags (at minimum 3), country, website, logo_colors

## Logo Rendering Standards
- Uniform height: 28-36px in proposals
- Default: grayscale filter with opacity 0.5
- Hover: full color with opacity 1.0
- Smooth 0.3s transition
- `object-fit: contain` for consistent sizing
