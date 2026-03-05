import os

logos_dir = "/Users/timstevens/Antigravity/logos"

svgs = {
    "protea": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50"><text x="100" y="34" text-anchor="middle" font-family="Georgia, serif" font-size="22" font-weight="700" fill="#8B6914" letter-spacing="3">PROTEA</text><text x="100" y="48" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="#8B6914" letter-spacing="5">HOTELS</text></svg>""",
    "sandals": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50"><text x="100" y="34" text-anchor="middle" font-family="Georgia, serif" font-size="26" font-weight="700" fill="#00457C" letter-spacing="2">SANDALS</text><text x="100" y="48" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#00457C" letter-spacing="4">RESORTS</text></svg>""",
    "sun_international": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 50"><circle cx="25" cy="25" r="15" fill="none" stroke="#C8982A" stroke-width="2"/><line x1="25" y1="5" x2="25" y2="10" stroke="#C8982A" stroke-width="2"/><line x1="25" y1="40" x2="25" y2="45" stroke="#C8982A" stroke-width="2"/><line x1="5" y1="25" x2="10" y2="25" stroke="#C8982A" stroke-width="2"/><line x1="40" y1="25" x2="45" y2="25" stroke="#C8982A" stroke-width="2"/><text x="140" y="22" text-anchor="middle" font-family="Georgia, serif" font-size="16" font-weight="700" fill="#1a1a2e" letter-spacing="2">SUN</text><text x="140" y="38" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="#1a1a2e" letter-spacing="3">INTERNATIONAL</text></svg>""",
    "oneandonly": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 50"><text x="110" y="22" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="#1a1a2e" letter-spacing="6">ONE&amp;ONLY</text><line x1="30" y1="28" x2="190" y2="28" stroke="#C8982A" stroke-width="0.5"/><text x="110" y="42" text-anchor="middle" font-family="Georgia, serif" font-size="9" fill="#8B8680" letter-spacing="4">RESORTS</text></svg>""",
    "dimension_data": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 50"><rect x="5" y="12" width="26" height="26" rx="3" fill="none" stroke="#E4002B" stroke-width="2.5"/><rect x="11" y="18" width="14" height="14" rx="2" fill="none" stroke="#E4002B" stroke-width="1.5"/><text x="140" y="22" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#1a1a2e" letter-spacing="1">Dimension</text><text x="140" y="38" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#E4002B" letter-spacing="1">Data</text></svg>"""
}

for name, svg_content in svgs.items():
    file_path = os.path.join(logos_dir, f"{name}.svg")
    with open(file_path, "w") as f:
        f.write(svg_content)
    print(f"Created {file_path}")
