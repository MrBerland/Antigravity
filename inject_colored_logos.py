import re
import base64
import os
import json

HTML_PATH = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V15.html'
LOGOS_DIR = '/Users/timstevens/Antigravity/logos'
REGISTRY_PATH = os.path.join(LOGOS_DIR, 'brand_registry.json')

file_logos = ['tigerbrands.png', 'discovery2.svg', 'abinbev.svg', 'pepsico.png', 'unilever_dark.svg', 'engen_favicon.png', 'kimberlyclark.svg']

with open(REGISTRY_PATH, 'r') as f:
    registry = json.load(f)

# Better SVG fallbacks for Shoprite and Old Mutual
shoprite_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 40" width="160"><text x="0" y="32" font-family="Arial, Helvetica, sans-serif" font-weight="800" font-size="32" fill="#E31837" letter-spacing="-1">SHOPRITE</text></svg>'
oldmutual_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 40" width="160"><text x="0" y="30" font-family="Arial, Helvetica, sans-serif" font-weight="900" font-size="28" fill="#003B29" letter-spacing="1">OLD MUTUAL</text></svg>'

def get_base64_svg(svg_str):
    b64 = base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}"

def get_base64(filename):
    ext = filename.split('.')[-1]
    mime = 'image/png' if ext == 'png' else 'image/svg+xml'
    path = os.path.join(LOGOS_DIR, filename)
    if os.path.exists(path):
        with open(path, 'rb') as lf:
            b64 = base64.b64encode(lf.read()).decode('utf-8')
        return f"data:{mime};base64,{b64}"
    return ""

img_tags = []

style = "height: 44px; object-fit: contain; max-width: 140px; padding: 6px 14px; background: rgba(255,255,255,0.95); border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); opacity: 0.9; transition: all 0.3s; cursor: default;"
hover_on = "this.style.opacity=1; this.style.transform='scale(1.05)'"
hover_off = "this.style.opacity=0.9; this.style.transform='none'"

img_tags.append(f'<img src="{get_base64_svg(shoprite_svg)}" style="{style}" onmouseover="{hover_on}" onmouseout="{hover_off}" alt="Shoprite">')
img_tags.append(f'<img src="{get_base64_svg(oldmutual_svg)}" style="{style}" onmouseover="{hover_on}" onmouseout="{hover_off}" alt="Old Mutual">')

for logo in file_logos:
    b64_uri = get_base64(logo)
    if b64_uri:
        img_tags.append(f'<img src="{b64_uri}" style="{style}" onmouseover="{hover_on}" onmouseout="{hover_off}" alt="{logo.split(".")[0]}">')

registry_ids = ['afrihost', 'dimension_data', 'sun_international']
for brand in registry['brands']:
    if brand.get('id') in registry_ids and 'logo_data_uri' in brand:
        img_tags.append(f'<img src="{brand["logo_data_uri"]}" style="{style}" onmouseover="{hover_on}" onmouseout="{hover_off}" alt="{brand.get("name","")}">')

logo_html = '\n'.join(img_tags)

css = """
                <div class="client-logo-strip" style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 24px; max-width: 1000px; margin: 0 auto;">
""" + '\n' + logo_html + '\n                </div>'

with open(HTML_PATH, 'r') as f:
    content = f.read()

# Replace existing logo strip (it spans from <style> to </div> underneath)
content = re.sub(
    r'<style>\s*\.client-logo-strip img.*?</div>\s*</div>',
    css + '\n            </div>',
    content,
    flags=re.DOTALL
)

# Now Let's update the testimonials
# 1. Read capeherb.png and tigerbrands.png properly for reviews
tiger_uri = get_base64('tigerbrands.png')
cape_uri = get_base64('capeherb.png')

# The review block has structure: <img src="data:image/svg+xml... alt="Tiger Brands">
# And <img src="data:image/png;base64... alt="Cape Herb and Spice">
review_style = "height: 36px; object-fit: contain; max-width: 120px; margin-left: auto; padding: 4px 10px; background: rgba(255,255,255,0.95); border-radius: 4px;"
new_tiger_img = f'<img src="{tiger_uri}" style="{review_style}" alt="Tiger Brands">'
new_cape_img = f'<img src="{cape_uri}" style="{review_style}" alt="Cape Herb and Spice">'

# Replace the inner image tags
content = re.sub(r'<img src="[^"]+" style="[^"]+" alt="Tiger Brands">', new_tiger_img, content)
content = re.sub(r'<img src="[^"]+" style="[^"]+" alt="Cape Herb and Spice">', new_cape_img, content)

with open(HTML_PATH, 'w') as f:
    f.write(content)

print("HTML modified successfully.")
