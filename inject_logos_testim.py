import re
import base64
import os
import json

HTML_PATH = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V15.html'
LOGOS_DIR = '/Users/timstevens/Antigravity/logos'
REGISTRY_PATH = os.path.join(LOGOS_DIR, 'brand_registry.json')

with open(REGISTRY_PATH, 'r') as f:
    registry = json.load(f)

# Collect 11 logos to use
# From files
file_logos = ['tigerbrands.svg', 'shoprite.svg', 'discovery2.svg', 'abinbev.svg', 'pepsico.png', 'unilever_dark.svg', 'engen_favicon.png', 'kimberlyclark.svg']

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
for logo in file_logos:
    b64_uri = get_base64(logo)
    if b64_uri:
        style = "height: 36px; object-fit: contain; max-width: 140px; opacity: 0.5; filter: grayscale(100%) brightness(200%); transition: opacity 0.3s;"
        # Increase size for tigerbrands slightly or we just use tigerbrands.svg which scales well
        img_tags.append(f'<img src="{b64_uri}" style="{style}" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.5" alt="{logo.split(".")[0]}">')

# From registry data_uris
registry_ids = ['afrihost', 'dimension_data', 'sun_international']
for brand in registry['brands']:
    if brand.get('id') in registry_ids and 'logo_data_uri' in brand:
        img_tags.append(f'<img src="{brand["logo_data_uri"]}" style="height: 36px; object-fit: contain; max-width: 140px; opacity: 0.5; filter: grayscale(100%) brightness(200%); transition: opacity 0.3s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.5" alt="{brand["name"]}">')

logo_html = '\n'.join(img_tags)
css = """
                <style>
                    .client-logo-strip img { height: 36px; margin: 0 10px; opacity: 0.4; transition: opacity 0.3s; filter: grayscale(100%) brightness(200%); cursor: default; }
                    .client-logo-strip img:hover { opacity: 0.8; }
                </style>
                <div class="client-logo-strip" style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 48px;">
""" + '\n' + logo_html + '\n                </div>'

with open(HTML_PATH, 'r') as f:
    content = f.read()

# Replace existing logo strip
content = re.sub(
    r'<style>\s*\.client-logo-strip img.*?</div>',
    css,
    content,
    flags=re.DOTALL
)

# Insert logos into testimonials
tiger_uri = get_base64('tigerbrands.svg')
cape_uri = get_base64('capeherb.png')

tiger_logo_img = f'<img src="{tiger_uri}" style="height:24px; object-fit:contain; filter:brightness(200%) grayscale(100%); margin-left: auto;" alt="Tiger Brands">'
cape_logo_img = f'<img src="{cape_uri}" style="height:24px; object-fit:contain; filter:brightness(200%) grayscale(100%); margin-left: auto;" alt="Cape Herb and Spice">'

# We need to find the <div style="display: flex; align-items: center; gap: 12px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px;">
# and insert the logo at the end of it

parts = content.split('<div style="display: flex; align-items: center; gap: 12px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px;">')

if len(parts) >= 3:
    # First split is before the first testim (Clinton Fouche)
    tiger_testim = parts[1]
    # Second split is before Rishendran Naidoo
    cape_testim = parts[2]
    
    # Insert at the end of the div
    tiger_testim = tiger_testim.replace('</div>\n                </div>', f'{tiger_logo_img}\n                    </div>\n                </div>', 1)
    cape_testim = cape_testim.replace('</div>\n                </div>', f'{cape_logo_img}\n                    </div>\n                </div>', 1)
    
    content = parts[0] + '<div style="display: flex; align-items: center; gap: 12px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px;">' + tiger_testim + '<div style="display: flex; align-items: center; gap: 12px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px;">' + cape_testim

with open(HTML_PATH, 'w') as f:
    f.write(content)

print("Done")
