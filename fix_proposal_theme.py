import re
import os
import base64
import json

HTML_PATH = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V15.html'
LOGOS_DIR = '/Users/timstevens/Antigravity/logos'
REGISTRY_PATH = os.path.join(LOGOS_DIR, 'brand_registry.json')

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update css classes / body classes
content = content.replace('<html lang="en" class="dark">', '<html lang="en" class="dark" style="scrollbar-width: none;">')

# 2. Add light/dark variables to :root, and define them
new_vars = """
        :root {
            --primary: #2463EB;
            --primary-hover: #1d4ed8;
            --accent: #0077B6;
            --accent-glow: rgba(0, 119, 182, 0.2);
            --bg-base: #f8fafc;
            --bg-surface: #ffffff;
            --bg-surface-elevated: #f1f5f9;
            --border: #e2e8f0;
            --border-light: rgba(0,0,0,0.05);
            --text-main: #334155;
            --text-muted: #64748b;
            --text-heading: #0f172a;
            --success: #10B981;
            --warning: #F59E0B;
            --danger: #EF4444;
            --bg-glass: rgba(255, 255, 255, 0.8);
            --bg-glass-sidebar: rgba(255, 255, 255, 0.7);

            --font-sans: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --radius-sm: 8px;
            --radius-md: 16px;
            --radius-lg: 24px;
        }

        html.dark {
            --primary: #2463EB;
            --primary-hover: #1d4ed8;
            --accent: #00D1FF;
            --accent-glow: rgba(0, 209, 255, 0.3);
            --bg-base: #020617;
            --bg-surface: #0f172a;
            --bg-surface-elevated: #1e293b;
            --border: #334155;
            --border-light: rgba(255,255,255,0.05);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-heading: #ffffff;
            --success: #10B981;
            --warning: #F59E0B;
            --danger: #EF4444;
            --bg-glass: rgba(15, 23, 42, 0.5);
            --bg-glass-sidebar: rgba(15, 23, 42, 0.6);
        }
"""
content = re.sub(r':root\s*\{[^}]+\}', new_vars, content, count=1)

# Modify basic layouts for scroll-snap
layout_css = """
        html, body {
            height: 100%;
            overflow: hidden;
        }
        
        .main-content {
            margin-left: 280px;
            height: 100vh;
            overflow-y: auto;
            scroll-behavior: smooth;
            scroll-snap-type: y mandatory;
            padding: 0;
            position: relative;
            scrollbar-width: thin;
            scrollbar-color: var(--border) transparent;
        }

        .section {
            scroll-snap-align: start;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
"""
content = re.sub(r'body\s*\{[^\}]+overflow-x:\s*hidden;\s*display:\s*flex;\s*\}', 'body {\n            font-family: var(--font-sans);\n            background-color: var(--bg-base);\n            color: var(--text-main);\n            line-height: 1.6;\n            -webkit-font-smoothing: antialiased;\n            display: flex;\n            height: 100%;\n            overflow: hidden;\n        }', content)
content = re.sub(r'\.main-content\s*\{[^\}]+\}', '.main-content {\n            margin-left: 280px;\n            flex: 1;\n            height: 100vh;\n            overflow-y: auto;\n            scroll-behavior: smooth;\n            scroll-snap-type: y mandatory;\n            padding: 0;\n            position: relative;\n        }', content)

content = content.replace('.section {\n            min-height: 100vh;\n            padding: 80px 120px;\n            position: relative;\n            z-index: 10;\n            border-bottom: 1px solid rgba(255, 255, 255, 0.05);\n        }', 
    '.section {\n            min-height: 100vh;\n            padding: 80px 120px;\n            position: relative;\n            z-index: 10;\n            border-bottom: 1px solid var(--border-light);\n            scroll-snap-align: start;\n        }')

# Add brand logo img classes
logo_css = """
        .brand-logo-img {
            height: 36px;
            object-fit: contain;
            max-width: 140px;
            opacity: 0.5;
            transition: all 0.3s ease;
        }
        html.dark .brand-logo-img {
            filter: brightness(200%) grayscale(100%);
        }
        html[class="dark"] .brand-logo-img {
            filter: brightness(200%) grayscale(100%);
        }
        html .brand-logo-img {
            filter: brightness(0%) grayscale(100%);
        }
        html.dark .brand-logo-img:hover, html .brand-logo-img:hover {
            opacity: 1;
        }
        
        .review-logo {
            height: 24px;
            margin-left: auto;
            object-fit: contain;
            opacity: 0.8;
        }
        html.dark .review-logo {
            filter: brightness(200%) grayscale(100%);
        }
        html .review-logo {
            filter: brightness(0%) grayscale(100%);
        }
"""
content = content.replace('/* BACKGROUND EFFECTS */', logo_css + '\n        /* BACKGROUND EFFECTS */')

# Generic replacements for hardcoded colors
content = content.replace('rgba(15, 23, 42, 0.6)', 'var(--bg-glass-sidebar)')
content = content.replace('rgba(15, 23, 42, 0.5)', 'var(--bg-glass)')
content = content.replace('rgba(255,255,255,0.05)', 'var(--border-light)')
content = content.replace('rgba(255, 255, 255, 0.05)', 'var(--border-light)')
content = content.replace('rgba(255,255,255,0.1)', 'var(--border-light)')
content = content.replace('rgba(255, 255, 255, 0.1)', 'var(--border-light)')
content = content.replace('rgba(255,255,255,0.03)', 'var(--bg-glass)')
content = content.replace('rgba(0,0,0,0.2)', 'var(--bg-glass)')

def repl_white(m):
    return m.group(0).replace('white', 'var(--text-heading)')
content = re.sub(r'color:\s*white;?', repl_white, content)
content = re.sub(r'color:\s*#fff;?', repl_white, content)

def repl_black(m):
    return m.group(0).replace('black', 'var(--bg-base)')
content = re.sub(r'color:\s*black;?', repl_black, content)


# Fix Logo Strip - Revert to Monochrome SVG/PNG
file_logos = ['tigerbrands.png', 'shoprite.svg', 'discovery2.svg', 'abinbev.svg', 'pepsico.png', 'unilever_dark.svg', 'engen_favicon.png', 'kimberlyclark.svg']

def get_base64(filename):
    path = os.path.join(LOGOS_DIR, filename)
    if os.path.exists(path):
        ext = filename.split('.')[-1]
        mime = 'image/png' if ext == 'png' else ('image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/svg+xml')
        with open(path, 'rb') as f_logo:
            b64 = base64.b64encode(f_logo.read()).decode('utf-8')
        return f"data:{mime};base64,{b64}"
    return ""

# Try loading the original Shoprite SVG if it exists, or generate standard one using generic text if shoprite is dead
shoprite_b64 = get_base64('shoprite.svg')
# the previous shoprite.svg was basic black Arial, which works perfect.

img_tags = []
for file in file_logos:
    b6 = get_base64(file)
    if b6:
        img_tags.append(f'<img src="{b6}" class="brand-logo-img" alt="{file.split(".")[0]}">')

# Also include registry items
with open(REGISTRY_PATH, 'r') as f_reg:
    reg_data = json.load(f_reg)

reg_ids = ['afrihost', 'dimension_data', 'sun_international', 'old_mutual'] # let's see if we have old_mutual inside registry
for b in reg_data.get('brands', []):
    if b.get('id') in reg_ids and b.get('logo_data_uri'):
        img_tags.append(f'<img src="{b["logo_data_uri"]}" class="brand-logo-img" alt="{b.get("name","")}">')

logo_html = '<div class="client-logo-strip" style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 48px; max-width: 1000px; margin: 0 auto;">\n' + '\n'.join(img_tags) + '\n</div>'

# Use a precise regex to replace only the logo strip div and its img tags.
# In inject_logos_testim.py the structure is:
# <div class="client-logo-strip"...>
# <img ...>
# ...
# </div>
content = re.sub(r'<div class="client-logo-strip"[^>]*>.*?</div>', logo_html, content, count=1, flags=re.DOTALL)

# Fix review logos
tiger_uri = get_base64('tigerbrands.png')
cape_uri = get_base64('capeherb.png')
if tiger_uri:
    content = re.sub(r'<img src="[^"]+" style="[^"]+" alt="Tiger Brands">', f'<img src="{tiger_uri}" class="review-logo" alt="Tiger Brands">', content)
if cape_uri:
    content = re.sub(r'<img src="[^"]+" style="[^"]+" alt="Cape Herb and Spice">', f'<img src="{cape_uri}" class="review-logo" alt="Cape Herb and Spice">', content)


# Add theme toggle button in sidebar below brand
toggle_html = """
        <div style="margin-bottom: 24px;">
            <button id="themeToggle" style="background: var(--bg-glass); border: 1px solid var(--border); color: var(--text-main); padding: 8px 16px; border-radius: var(--radius-sm); cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 0.85rem; width: 100%; justify-content: flex-start; transition: all 0.3s; font-family: var(--font-mono);">
                <svg id="moonIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: block;">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
                <svg id="sunIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
                <span id="themeText">Dark Mode</span>
            </button>
        </div>
"""
# insert toggle after <div class="brand">...</div>
content = re.sub(r'(<div class="brand">.*?</div>)', r'\1\n' + toggle_html, content, flags=re.DOTALL)


js_code = """
        // Theme Toggle
        const themeToggle = document.getElementById('themeToggle');
        const html = document.documentElement;
        const sunIcon = document.getElementById('sunIcon');
        const moonIcon = document.getElementById('moonIcon');
        const themeText = document.getElementById('themeText');

        themeToggle.addEventListener('click', () => {
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                html.classList.add('light'); // Just to be explicit
                sunIcon.style.display = 'block';
                moonIcon.style.display = 'none';
                themeText.textContent = 'Light Mode';
            } else {
                html.classList.add('dark');
                html.classList.remove('light');
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'block';
                themeText.textContent = 'Dark Mode';
            }
        });

        // Simple Intersection Observer to highlight active navigation link
        document.addEventListener('DOMContentLoaded', () => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
                        const id = entry.target.getAttribute('id');
                        document.querySelectorAll('.nav-links a').forEach(link => {
                            link.classList.remove('active');
                            if (link.getAttribute('href') === `#${id}`) {
                                link.classList.add('active');
                            }
                        });
                    }
                });
            }, { 
                root: document.querySelector('.main-content'),
                threshold: 0.5 
            });

            document.querySelectorAll('.section').forEach(section => {
                observer.observe(section);
            });
        });
"""
content = re.sub(r'// Simple Intersection Observer.*}\);\s*}\);', js_code, content, flags=re.DOTALL)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML modified successfully.")
