#!/usr/bin/env python3
"""
Replace ALL emoji icons in CFAO Proposal V13 with custom on-brand SVG icons.
Matches existing Feather icon style: 24×24 viewBox, stroke-based, stroke-width 2,
round caps and joins, fill none, currentColor.
"""
import re

HTML_FILE = "/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V13.html"

# ════════════════════════════════════════════════════════
# ICON LIBRARY — Feather-style, 24×24 viewBox
# stroke-width: 2, stroke-linecap: round, stroke-linejoin: round
# fill: none, stroke: currentColor
# ════════════════════════════════════════════════════════

ICONS = {
    # ── REPORTS & ANALYTICS ──
    "technical_analysis": '''<svg class="icon" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>''',

    "cost_breakdown": '''<svg class="icon" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>''',

    "time_of_use": '''<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>''',

    "consumption_breakdown": '''<svg class="icon" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="3" y1="20" x2="21" y2="20"/></svg>''',

    "after_hours": '''<svg class="icon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>''',

    "carbon_esg": '''<svg class="icon" viewBox="0 0 24 24"><path d="M12 22c4-4 8-7.5 8-12a8 8 0 1 0-16 0c0 4.5 4 8 8 12z"/><path d="M12 12c-1.5-2-3-3-5-3" style="fill:none;"/><path d="M12 16c1.5-2 3-4 5-4" style="fill:none;"/></svg>''',

    "smart_alert": '''<svg class="icon" viewBox="0 0 24 24"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>''',

    "ai_data_export": '''<svg class="icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>''',

    # ── STRATEGIC / OUTCOME ──
    "trend_down": '''<svg class="icon" viewBox="0 0 24 24"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg>''',

    "cost_visibility": '''<svg class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><path d="M14 10.5a2.5 2.5 0 0 0-2.5-2.5H10a2.5 2.5 0 0 0 0 5h2a2.5 2.5 0 0 1 0 5h-2.5a2.5 2.5 0 0 1-2.5-2.5"/></svg>''',

    "fleet_oversight": '''<svg class="icon" viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>''',

    # ── TECHNOLOGY / DATA ──
    "microscope": '''<svg class="icon" viewBox="0 0 24 24"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 0 0 0-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6"/><circle cx="9" cy="4" r="2"/></svg>''',

    "rocket": '''<svg class="icon" viewBox="0 0 24 24"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 3 0 3 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-3 0-3"/></svg>''',

    "historical_depth": '''<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>''',

    "realtime": '''<svg class="icon" viewBox="0 0 24 24"><polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>''',

    "api_link": '''<svg class="icon" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>''',

    "security": '''<svg class="icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>''',

    "wrench": '''<svg class="icon" viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>''',
}


# ════════════════════════════════════════════════════════
# ICON CONTAINER — wraps SVG in branded circle bg
# ════════════════════════════════════════════════════════

def icon_container(svg_str, color="var(--color-primary)", bg_opacity="0.08", size="36px"):
    """Wrap an SVG icon in a brand-styled container."""
    return (
        f'<div style="width: {size}; height: {size}; border-radius: 10px; '
        f'background: rgba(36,99,235,{bg_opacity}); display: flex; align-items: center; '
        f'justify-content: center; color: {color}; margin-bottom: 10px; flex-shrink: 0;">'
        f'{svg_str}</div>'
    )


# ════════════════════════════════════════════════════════
# REPLACEMENTS
# ════════════════════════════════════════════════════════

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

count = 0

# ── 1. Report grid icons (lines ~2394-2429) ──
# Pattern: <div style="font-size: 1.2rem; margin-bottom: 8px;">EMOJI</div>

report_emoji_map = [
    ("📈", "technical_analysis"),
    ("💰", "cost_breakdown"),
    ("⏱️", "time_of_use"),
    ("📊", "consumption_breakdown"),
    ("🌙", "after_hours"),
    ("🌱", "carbon_esg"),
    ("🔔", "smart_alert"),
    ("📱", "ai_data_export"),
]

for emoji, icon_key in report_emoji_map:
    old = f'<div style="font-size: 1.2rem; margin-bottom: 8px;">{emoji}</div>'
    new = icon_container(ICONS[icon_key])
    if old in html:
        html = html.replace(old, new, 1)
        count += 1
        print(f"  ✓ {emoji} → {icon_key}")

# ── 2. Strategic outcome icons (lines ~1320-1332) ──
outcome_replacements = [
    ("📉 15% Consumption Reduction Target", ICONS["trend_down"], "15% Consumption Reduction Target"),
    ("💰 Complete Cost Visibility", ICONS["cost_visibility"], "Complete Cost Visibility"),
    ("🌱 Automated Carbon & Compliance Reporting", ICONS["carbon_esg"], "Automated Carbon & Compliance Reporting"),
    ("📡 100-Site Fleet Oversight", ICONS["fleet_oversight"], "100-Site Fleet Oversight"),
]

for old_text, svg, new_text in outcome_replacements:
    if old_text in html:
        inline_svg = svg.replace('class="icon"', 'class="icon" style="width:16px;height:16px;vertical-align:-3px;margin-right: 4px;"')
        html = html.replace(old_text, f'{inline_svg} {new_text}', 1)
        count += 1
        print(f"  ✓ {old_text[:30]}...")

# ── 3. Dashboard label icons ──
# Carbon & Compliance label
old_carbon_label = '🌱 Carbon & Compliance'
if old_carbon_label in html:
    inline_svg = ICONS["carbon_esg"].replace('class="icon"',
        'class="icon" style="width:14px;height:14px;vertical-align:-2px;margin-right:2px;"')
    html = html.replace(old_carbon_label, f'{inline_svg} Carbon & Compliance', 1)
    count += 1
    print(f"  ✓ Dashboard: Carbon & Compliance label")

# After-hours alert icon
old_moon = '<div class="alert-icon close-down">🌙</div>'
if old_moon in html:
    moon_svg = ICONS["after_hours"].replace('class="icon"',
        'class="icon" style="width:16px;height:16px;"')
    html = html.replace(old_moon, f'<div class="alert-icon close-down">{moon_svg}</div>', 1)
    count += 1
    print(f"  ✓ Dashboard: After-hours alert icon")

# ── 4. System Investment Breakdown heading ──
old_invest = '🛠️ System Investment Breakdown'
if old_invest in html:
    inline_svg = ICONS["wrench"].replace('class="icon"',
        'class="icon" style="width:18px;height:18px;vertical-align:-3px;margin-right:4px;"')
    html = html.replace(old_invest, f'{inline_svg} System Investment Breakdown', 1)
    count += 1
    print(f"  ✓ Investment heading: wrench icon")

# ── 5. Deployment option icons ──
deploy_replacements = [
    ("🔬", "microscope"),
    ("🚀", "rocket"),
]

for emoji, icon_key in deploy_replacements:
    old = f'>{emoji}</div>'
    if old in html:
        svg = ICONS[icon_key].replace('class="icon"',
            'class="icon" style="width:20px;height:20px;"')
        html = html.replace(old, f'>{svg}</div>', 1)
        count += 1
        print(f"  ✓ Deployment: {emoji} → {icon_key}")

# ── 6. Data architecture feature labels ──
arch_replacements = [
    ("📊 Unlimited Historical Depth", ICONS["historical_depth"], "Unlimited Historical Depth"),
    ("⚡ Real-Time Processing", ICONS["realtime"], "Real-Time Processing"),
    ("🔗 Open API Ecosystem", ICONS["api_link"], "Open API Ecosystem"),
    ("🔒 Enterprise Security", ICONS["security"], "Enterprise Security"),
]

for old_text, svg, new_text in arch_replacements:
    if old_text in html:
        inline_svg = svg.replace('class="icon"',
            'class="icon" style="width:14px;height:14px;vertical-align:-2px;margin-right:3px;"')
        html = html.replace(old_text, f'{inline_svg} {new_text}', 1)
        count += 1
        print(f"  ✓ Architecture: {old_text[:30]}...")

# ── 7. Catch any remaining emojis we missed ──
remaining_emojis = re.findall(r'[\U0001F300-\U0001F9FF][\uFE0F]?', html)
if remaining_emojis:
    print(f"\n  ⚠️  {len(remaining_emojis)} remaining emojis found: {remaining_emojis}")
else:
    print(f"\n  ✅ No remaining emojis!")

# Write back
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ Replaced {count} emoji icons with on-brand SVGs")
