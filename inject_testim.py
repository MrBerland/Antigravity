import re
import base64
import os

HTML_PATH = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V15.html'
LOGOS_DIR = '/Users/timstevens/Antigravity/logos'

with open(HTML_PATH, 'r') as f:
    content = f.read()

# Base64 encode logos
logos = ['tigerbrands.png', 'shoprite.svg', 'discovery2.svg', 'abinbev.svg', 'pepsico.png', 'unilever_dark.svg']

img_tags = []
for logo in logos:
    ext = logo.split('.')[-1]
    mime = 'image/png' if ext == 'png' else 'image/svg+xml'
    path = os.path.join(LOGOS_DIR, logo)
    with open(path, 'rb') as lf:
        b64 = base64.b64encode(lf.read()).decode('utf-8')
    img_tags.append(f'<img src="data:{mime};base64,{b64}" style="height: 32px; object-fit: contain; max-width: 140px; opacity: 0.5; filter: grayscale(100%) brightness(200%); transition: opacity 0.3s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.5" alt="{logo.split(".")[0]}">')

logo_html = '\n'.join(img_tags)

css = """
                <style>
                    .client-logo-strip img { height: 32px; opacity: 0.4; transition: opacity 0.3s; filter: grayscale(100%) brightness(200%); cursor: default; }
                    .client-logo-strip img:hover { opacity: 0.8; }
                </style>
                <div class="client-logo-strip" style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 48px;">
""" + '\n' + logo_html + '\n                </div>'

content = re.sub(
    r'<style>\s*\.client-logo-strip sv.*?</div>',
    css,
    content,
    flags=re.DOTALL
)

testimonials = """
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 60px;">
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 32px; border-radius: 12px; position: relative;">
                    <div style="color: var(--accent); font-size: 3rem; font-family: serif; position: absolute; top: 16px; left: 24px; opacity: 0.2; line-height: 1;">&ldquo;</div>
                    <div style="display: flex; gap: 4px; color: #FBBF24; margin-bottom: 16px;">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                    </div>
                    <p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 24px; position: relative; z-index: 1;">
                        "Awesome customer service, very insightful. So much value added since partnering with Augos and the information and opportunity the site creates is just unreal."
                    </p>
                    <div style="display: flex; align-items: center; gap: 12px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background: rgba(0,209,255,0.1); display: flex; align-items: center; justify-content: center; color: var(--accent); font-weight: bold; font-size: 1.1rem;">C</div>
                        <div>
                            <div style="color: white; font-weight: 600; font-size: 0.9rem;">Clinton Fouche</div>
                            <div style="color: var(--text-muted); font-size: 0.8rem;">Tiger Brands</div>
                        </div>
                    </div>
                </div>

                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 32px; border-radius: 12px; position: relative;">
                    <div style="color: var(--accent); font-size: 3rem; font-family: serif; position: absolute; top: 16px; left: 24px; opacity: 0.2; line-height: 1;">&ldquo;</div>
                    <div style="display: flex; gap: 4px; color: #FBBF24; margin-bottom: 16px;">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                    </div>
                    <p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 24px; position: relative; z-index: 1;">
                        "Met with the Augos team at their premise this morning. Was a great experience. Warm people with great insight and knowledge of the product and services they offer... Really impressed with their service as always."
                    </p>
                    <div style="display: flex; align-items: center; gap: 12px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background: rgba(0,209,255,0.1); display: flex; align-items: center; justify-content: center; color: var(--accent); font-weight: bold; font-size: 1.1rem;">R</div>
                        <div>
                            <div style="color: white; font-weight: 600; font-size: 0.9rem;">Rishendran Naidoo</div>
                            <div style="color: var(--text-muted); font-size: 0.8rem;">Cape Herb & Spice</div>
                        </div>
                    </div>
                </div>
            </div>
"""

content = content.replace('<!-- SECTION 05: HARDWARE -->', testimonials + '\n        <!-- SECTION 05: HARDWARE -->')

with open(HTML_PATH, 'w') as f:
    f.write(content)

print("Done")
