---
description: Create and manage on-brand SVG icons following the Augos design system
---

# Icon Creation & Management Workflow

// turbo-all

Custom SVG icons for Augos follow a strict Feather-style design spec. This workflow defines how to create new icons, register them, and embed them in HTML documents.

## Icon Registry

All icons are catalogued at `/Users/timstevens/Antigravity/icons/icon_registry.json` with:
- **name** — Human-readable icon name
- **category** — `reports`, `strategic`, `deployment`, `data`, `system`
- **tags** — Searchable keywords for flexible queries
- **svg** — Complete SVG markup ready for inline use
- **description** — What the icon represents

## Design Spec

Every icon MUST follow these rules:

```
viewBox="0 0 24 24"
stroke-width: 2
stroke: currentColor
fill: none
stroke-linecap: round
stroke-linejoin: round
CSS class: "icon"
```

### Key Rules
1. **Stroke-only** — Never use filled shapes. All visual weight comes from strokes.
2. **2px stroke** at 24px default size
3. **Round caps and joins** — No sharp terminators
4. **currentColor** — Icons inherit color from their parent container
5. **Minimal paths** — Keep path count low for clarity at small sizes
6. **2px minimum gap** between parallel strokes
7. **2px minimum corner radius** on rectangles

### Size Variants
| Size | Dimensions | Usage |
|------|-----------|-------|
| `sm` | 14×14px | Inline with text labels |
| `md` | 20×20px | Section headings, list items |
| `default` | 24×24px | Card icons, standalone |
| `lg` | 32×32px | Feature highlights, hero sections |

### Branded Container
For card/feature use, wrap icons in the standard container:
```html
<div style="width: 36px; height: 36px; border-radius: 10px; 
     background: rgba(36,99,235,0.08); display: flex; align-items: center; 
     justify-content: center; color: var(--color-primary); margin-bottom: 10px;">
  <svg class="icon" viewBox="0 0 24 24">...</svg>
</div>
```

### Inline Usage
For inline text labels:
```html
<svg class="icon" viewBox="0 0 24 24" style="width:14px;height:14px;vertical-align:-2px;margin-right:3px;">
  ...paths...
</svg> Label Text
```

## Steps for Creating a New Icon

1. Read the icon registry to check if a suitable icon already exists:
```bash
python3 -c "import json; [print(f'{k}: {v[\"name\"]} — {v[\"description\"]}') for k,v in json.load(open('/Users/timstevens/Antigravity/icons/icon_registry.json'))['icons'].items()]"
```

2. If no suitable icon exists, design a new one following the spec above. The SVG should:
   - Use only `path`, `line`, `polyline`, `circle`, and `rect` elements
   - Avoid `text`, `image`, or embedded rasters
   - Be recognizable at 14px (the smallest inline size)
   - Work in both light and dark contexts (stroke-only, currentColor)

3. Test the icon inline in HTML to verify it renders correctly at all sizes

4. Add the new icon to `icon_registry.json` with full metadata:
   - name, category, tags (minimum 3), description, svg

5. If replacing emojis in an existing document, use the replacement script pattern from `replace_emoji_icons.py`

## Query Examples
- "I need a chart icon" → check tags for `chart`, `analytics`
- "deployment icon" → filter `category == 'deployment'`
- "something for costs" → check tags for `cost`, `money`, `financial`
