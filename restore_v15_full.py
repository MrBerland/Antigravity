import re
import os

HTML_PATH = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V15.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update Matrix tooltip to display directly
matrix_old = '<div class="matrix-tooltip">'
matrix_new = '<div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">'
c = c.replace(matrix_old, matrix_new)

# 2. Insert everything before <!-- SECTION 07: DEPLOYMENT -->
insert_marker = '        <!-- SECTION 07: DEPLOYMENT -->'

new_blocks = """
        <div style="background: rgba(15, 23, 42, 0.5); border-left: 4px solid var(--accent); padding: 24px; border-radius: 8px; margin-top: 40px; margin-bottom: 40px;">
            <h4 style="color: white; margin-bottom: 12px; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2">
                    <line x1="12" y1="2" x2="12" y2="22"></line>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
                The "Operational Blind-Spot" ROI Formula
            </h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 0;">
                Imagine a wash-bay circulation pump, showroom spot-lights, and an industrial 3-phase compressor inadvertently left running on an empty dealership floor, every single night and weekend. Over a year, this invisible, constant 5 kW of baseload burns <strong>R157,023</strong> in pure electricity waste.
                <br><br>
                If the algorithmic tool needed to detect and eliminate this operational blind-spot costs you <strong>R3,000</strong> a year per site, you don't need a complex corporate spreadsheet to prove the business case:
                <br><br>
                <span style="color: white; font-family: 'JetBrains Mono', monospace; background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 4px; display: inline-block; margin-top: 8px;">
                    ROI = (Money saved from stopping the leak) ÷ (Annual Cost of the Augos Platform)
                </span>
            </p>
        </div>

        <h3 style="color:white; font-size:1.25rem; margin-top:48px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 16px;">
            5-Year Cumulative Impact (100 Site Fleet)</h3>
        <p style="font-size: 0.95rem; color: var(--text-muted); margin-top: 16px;">
            Calculated on a conservative <strong>2 kW average waste reduction</strong> per dealership, accounting
            for a 12% YoY utility tariff escalation against fixed SaaS operational costs.
        </p>

        <div class="grid-3" style="margin-top: 24px;">
            <div class="feature-card" style="padding: 24px; border: 1px dashed rgba(255,255,255,0.2); background: transparent;">
                <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Break-Even Period</div>
                <div style="font-size:2rem; color:white; font-weight:800; margin-bottom:8px;">1.8 <span style="font-size:1.2rem; font-weight:500; color:var(--text-muted);">Months</span></div>
                <div style="font-size:0.85rem; color:var(--text-muted);">System pays for itself by Week 8 based on R6.28M initial annualized gross savings.</div>
            </div>
            <div class="feature-card" style="padding: 24px;">
                <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Year 3 Cumulative Cashflow</div>
                <div style="font-size:2rem; color:var(--success); font-weight:800; margin-bottom:8px;">+ R20.2M</div>
                <div style="font-size:0.85rem; color:var(--text-muted);">Total net cash liquidity restored across the portfolio within 36 months.</div>
            </div>
            <div class="feature-card" style="padding: 24px; border: 1px solid var(--accent); background: rgba(0, 209, 255, 0.05);">
                <div style="font-size:0.8rem; color:var(--accent); text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">5-Year Net Present Value</div>
                <div style="font-size:2rem; color:var(--success); font-weight:800; margin-bottom:8px;">+ R28.5M</div>
                <div style="font-size:0.85rem; color:white;">Total 5-Year NPV calculated with a standard 10% corporate discount rate.</div>
            </div>
        </div>

    </section>

    <!-- SECTION 17: PRICING -->
    <section id="pricing" class="section">
        <div class="section-header">
            <span class="section-number">17</span>
            <h2 class="section-title">Enterprise Commercials & SaaS Models</h2>
        </div>
        <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
            Flexible commercial structures designed around OPEX optimization. Choose immediate capital acquisition
            or a fully managed Hardware-as-a-Service (HaaS) subscription across the entire multi-site portfolio.
        </p>
        <div class="grid-2">
            <div class="feature-card" style="border: 1px solid rgba(255,255,255,0.05);">
                <div style="font-size: 0.8rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); margin-bottom:12px;">Capex Hardware + SaaS</div>
                <div style="font-size:2rem; font-weight:800; color:white; margin-bottom:8px;">R3,750 <span style="font-size: 1rem; font-weight:400; color:var(--text-muted);">once-off / site</span></div>
                <div style="font-size:1.5rem; font-weight:700; color:var(--primary); margin-bottom:24px;">R250 <span style="font-size: 0.9rem; font-weight:400; color:var(--text-muted);">mo / meter</span></div>
                <ul style="list-style:none; padding:0; display:flex; flex-direction:column; gap:12px; font-size:0.9rem; color:var(--text-muted);">
                    <li style="display:flex;gap:8px;"><svg width="16" height="16" style="color:var(--primary);flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12" /></svg> Augos Nova Asset Ownership</li>
                    <li style="display:flex;gap:8px;"><svg width="16" height="16" style="color:var(--primary);flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12" /></svg> Unlimited Platform Users</li>
                    <li style="display:flex;gap:8px;"><svg width="16" height="16" style="color:var(--primary);flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12" /></svg> 5 Years Data Hosting Included</li>
                    <li style="display:flex;gap:8px;"><svg width="16" height="16" style="color:var(--primary);flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12" /></svg> Live ADK Agent Access</li>
                </ul>
            </div>
            <div class="feature-card" style="border: 1px solid var(--accent); background: rgba(0, 209, 255, 0.05); position:relative; overflow:hidden;">
                <div style="position:absolute; top:20px; right:20px; background:var(--accent); color:black; font-size:0.7rem; font-weight:800; padding:4px 12px; border-radius:100px; text-transform:uppercase;">Recommended OPEX</div>
                <div style="font-size: 0.8rem; text-transform:uppercase; letter-spacing:1px; color:var(--accent); margin-bottom:12px;">Hardware-as-a-Service (HaaS)</div>
                <div style="font-size:2rem; font-weight:800; color:white; margin-bottom:8px;">R0 <span style="font-size: 1rem; font-weight:400; color:var(--text-muted);">upfront capex</span></div>
                <div style="font-size:1.5rem; font-weight:700; color:var(--accent); margin-bottom:24px;">R495 <span style="font-size: 0.9rem; font-weight:400; color:var(--text-muted);">mo / meter*</span></div>
                <ul style="list-style:none; padding:0; display:flex; flex-direction:column; gap:12px; font-size:0.9rem; color:var(--text-muted);">
                    <li style="display:flex;gap:8px; color:white;"><svg width="16" height="16" style="color:var(--accent);flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12" /></svg> Meter Hardware Included</li>
                    <li style="display:flex;gap:8px; color:white;"><svg width="16" height="16" style="color:var(--accent);flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12" /></svg> Lifetime Hardware Warranty (Swaps)</li>
                    <li style="display:flex;gap:8px;"><svg width="16" height="16" style="color:var(--accent);flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12" /></svg> White-Label Dashboard Support</li>
                    <li style="display:flex;gap:8px;"><svg width="16" height="16" style="color:var(--accent);flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12" /></svg> Dedicated Account Executive</li>
                </ul>
                <div style="font-size: 0.75rem; color:var(--text-muted); margin-top:24px;">*Contracted over 36 months, bulk 100-site discount applied. Local installation cost excluded.</div>
            </div>
        </div>
"""

# Replace the closing </section> of section 06 with the new blocks!
c = c.replace('    </section>\n\n    <!-- SECTION 07: DEPLOYMENT -->', new_blocks + '\n\n    <!-- SECTION 18: DEPLOYMENT -->')

# Update the deployment number to 18
c = c.replace('<span class="section-number">07</span>', '<span class="section-number">18</span>')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(c)

print("V15 Restored")

