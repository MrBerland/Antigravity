"""
V13 CLEAN REBUILD — Extract balanced sections from V12,
restructure into new narrative order, verify div balance.

Strategy: Don't use regex to strip section headers. Instead, for each
V12 section block, find the line after the section-header closing </div>
and take everything from there to just before </section>.
"""

SRC = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V12.html'
OUT = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V13.html'

with open(SRC) as f:
    lines = f.readlines()

def grab(s, e):
    """Lines s..e (1-indexed, inclusive), joined with newlines."""
    return ''.join(lines[s-1:e])

def div_balance(text):
    return text.count('<div') - text.count('</div')

def extract_section_body(start, end):
    """Given V12 section line range (1-indexed, inclusive),
    return just the inner content — stripping <section>, section-header, and </section>."""
    
    # Find where section-header ends
    body_start = None
    header_depth = 0
    in_header = False
    
    for i in range(start - 1, end):  # 0-indexed
        line = lines[i]
        stripped = line.strip()
        
        if 'class="section-header"' in stripped:
            in_header = True
            header_depth = 0
        
        if in_header:
            header_depth += line.count('<div') - line.count('</div')
            if header_depth <= 0:
                # Header div is closed, content starts on next line
                body_start = i + 2  # next line, 1-indexed
                break
    
    if body_start is None:
        # No section-header found, start after <section> line
        body_start = start + 1
    
    # End is one line before </section>
    body_end = end - 1
    
    # Skip any blank lines at the start
    while body_start <= body_end and lines[body_start - 1].strip() == '':
        body_start += 1
    
    content = grab(body_start, body_end)
    return content

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXTRACT V12 BLOCKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Header: everything before first section (CSS, <header>, <div class="container">)
header = grab(1, 1307)

# Sections (line ranges from V12 structure scan):
sec_ranges = {
    'roi':      (1308, 1501),   # "Beyond the Hike" — ROI/savings
    'retail':   (1505, 1575),   # "Specialist Retail Intelligence"
    'platform': (1594, 1845),   # "Augos Intelligence Platform" — UI mockups
    'hardware': (1848, 2007),   # "Hardware Enabler"
    'fleet':    (2011, 2155),   # "Active Fleet Management"
    'exec':     (2158, 2246),   # "Execution & Phase 1 Scope" — NERSA
    'deploy':   (2249, 2285),   # "Deployment Strategy"
    'compete':  (2289, 2341),   # "Competitive Overview"
    'about':    (2344, 2385),   # "About Augos"
    'cta':      (2388, 2406),   # CTA
}

# Extract and verify each section
bodies = {}
print("Section extractions:")
for name, (s, e) in sec_ranges.items():
    full = grab(s, e)
    body = extract_section_body(s, e)
    full_bal = div_balance(full)
    body_bal = div_balance(body)
    print(f"  {name:12s}: full={full_bal:+d} {'✅' if full_bal==0 else '❌'}  body={body_bal:+d} {'✅' if body_bal==0 else '❌'}")
    bodies[name] = body

# Footer
footer = grab(2408, len(lines))  # starts with </div> (container close), then footer div, script, etc.

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BUILD NEW V13 SECTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def make_section(num, title, content):
    """Wrap content in a section with header. Content is already indented."""
    return f'''
        <!-- {num}. {title.upper()} -->
        <section>
            <div class="section-header">
                <div class="section-num">{num:02d}</div>
                <h2 class="section-title">{title}</h2>
            </div>

{content}
        </section>

'''

# ── SECTION 01: Expected Outcomes (NEW content) ──
outcomes_content = '''\
            <p>By deploying the Augos Energy Intelligence Platform across CFAO Mobility's national dealership network, the following measurable outcomes are delivered within the first operational year:</p>

            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 32px 0;">
                <div class="content-card" style="border-left: 4px solid var(--color-success); margin: 0;">
                    <h4 style="color: var(--color-success); margin-bottom: 8px;">📉 15% Consumption Reduction Target</h4>
                    <p style="font-size: 14px; color: var(--color-muted); margin: 0;">Achieved through automated after-hours baseload detection, real-time anomaly alerting, and portfolio-wide benchmarking. Validated by historical deployments across equivalent retail portfolios.</p>
                </div>
                <div class="content-card" style="border-left: 4px solid var(--color-primary); margin: 0;">
                    <h4 style="color: var(--color-primary); margin-bottom: 8px;">💰 Complete Cost Visibility</h4>
                    <p style="font-size: 14px; color: var(--color-muted); margin: 0;">Every dealership's electricity cost is calculated in real-time using live municipal tariff structures — no more waiting for monthly statements or reconciling inaccurate utility bills.</p>
                </div>
                <div class="content-card" style="border-left: 4px solid #10b981; margin: 0;">
                    <h4 style="color: #10b981; margin-bottom: 8px;">🌱 Automated Carbon & Compliance Reporting</h4>
                    <p style="font-size: 14px; color: var(--color-muted); margin: 0;">Scope 2 emissions calculated continuously, providing the data layer for Carbon Tax Phase 2 and mandatory Energy Performance Certificates (SANS 1544).</p>
                </div>
                <div class="content-card" style="border-left: 4px solid #f59e0b; margin: 0;">
                    <h4 style="color: #f59e0b; margin-bottom: 8px;">📡 100-Site Fleet Oversight</h4>
                    <p style="font-size: 14px; color: var(--color-muted); margin: 0;">Every meter monitored for connectivity, firmware status, and data latency. Local electricians handle physical intervention via our guided mobile app — no specialist travel costs.</p>
                </div>
            </div>

            <div class="callout callout-success">
                <div class="callout-icon">
                    <svg class="icon icon-lg" viewBox="0 0 24 24">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                        <polyline points="22 4 12 14.01 9 11.01" />
                    </svg>
                </div>
                <div class="callout-content">
                    <h3>Phase 1 Focus: Main Electricity Incomers</h3>
                    <p>This initial deployment targets the primary electricity incomer at each dealership. <strong>Note:</strong> The platform seamlessly scales to sub-metering, water monitoring, and generator measurement as future phases dictate.</p>
                </div>
            </div>
'''

sec01 = make_section(1, 'Expected Outcomes for CFAO Mobility', outcomes_content)

# ── SECTION 02: The Complete Augos Service ──
# Combines: retail intel + dealership hero + hardware + fleet
# Add sub-headings for each merged block
service_parts = []
service_parts.append('''\
            <p>Augos delivers a fully managed energy intelligence service — not just hardware, not just software, but a unified operational capability purpose-built for multi-site automotive retail.</p>

            <h3 style="margin-top: 40px; margin-bottom: 16px; color: var(--color-primary);">Specialist Retail Intelligence</h3>
''')
service_parts.append(bodies['retail'])
service_parts.append('''
            <div class="content-card" style="margin: 40px 0; padding: 40px;">
                <h3 style="font-size: 1.5rem; margin-bottom: 12px; letter-spacing: -0.02em;">Intelligence Where It Matters — On the Showroom Floor</h3>
                <p style="margin-bottom: 24px; max-width: 720px; color: var(--color-muted);">The Augos platform delivers real-time energy alerts and AI insights directly to your mobile device. A CFAO dealership principal can review live consumption anomalies, respond to after-hours baseload breaches, and verify resolution — all without leaving the showroom floor.</p>
                <div style="border-radius: 12px; overflow: hidden; box-shadow: var(--shadow);">
                    <img src="dealership_app_hero.jpg" alt="CFAO Dealership Manager viewing Augos energy alerts on mobile" style="width: 100%; display: block; object-fit: cover; max-height: 420px;" />
                </div>
            </div>

            <h3 style="margin-top: 40px; margin-bottom: 16px; color: var(--color-primary);">The Hardware Kit</h3>
''')
service_parts.append(bodies['hardware'])
service_parts.append('''
            <h3 style="margin-top: 40px; margin-bottom: 16px; color: var(--color-primary);">National Fleet Oversight</h3>
''')
service_parts.append(bodies['fleet'])

service_content = '\n'.join(service_parts)
sec02 = make_section(2, 'The Complete Augos Service', service_content)

# ── SECTION 03: The Platform Experience ──
platform_lead = '''\
            <p>While gathering accurate data is essential, <strong>the true differentiator of Augos is the software platform itself</strong>. Below is a representative view of the live platform interface — from intelligent alerting to executive-level portfolio dashboards.</p>
'''
sec03 = make_section(3, 'The Platform Experience', platform_lead + '\n' + bodies['platform'])

# ── SECTION 04: The Regulatory Tailwind ──
reg_lead = '''\
            <p>CFAO Mobility operates one of the country's largest automotive retail networks — over 100 dealership sites representing 35+ OEM brands across all 9 provinces. Each is an energy-intensive facility. With municipal small business rates now averaging over <strong>412.00 c/kWh</strong> (including 15% VAT), the most expensive energy is no longer the units you use — it's the units you waste because you can't see them.</p>
'''
sec04 = make_section(4, 'The Regulatory Tailwind: Why Now', reg_lead + '\n' + bodies['exec'])

# ── SECTION 05: Investment & ROI ──
roi_lead = '''\
            <p>The barrier to entry for energy intelligence is exceptionally low compared to the potential savings. The following scenarios demonstrate how small, actionable data-driven adjustments translate into immediate bottom-line improvements.</p>
'''
roi_callout = '''
            <div class="callout callout-accent" style="margin-top: 32px; background: rgba(16,185,129,0.05); border-left-color: var(--color-success);">
                <div class="callout-icon" style="color: var(--color-success);">
                    <svg class="icon icon-lg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <div class="callout-content">
                    <h3 style="color: var(--color-success);">Data as a Clean Fuel</h3>
                    <p>For CFAO Mobility, the implementation of a retail-focused measurement system is the first step in converting high-cost utility bills into high-value operational data. In an environment of 412 c/kWh, data isn\'t just information — it\'s the most profitable fuel you have.</p>
                </div>
            </div>
'''
sec05 = make_section(5, 'Investment & Return', roi_lead + '\n' + bodies['roi'] + '\n' + roi_callout)

# ── SECTION 06: Deployment Strategy ──
sec06 = make_section(6, 'Deployment Strategy', bodies['deploy'])

# ── SECTION 07: Why Augos ──
sec07 = make_section(7, 'Why Augos', bodies['compete'] + '\n' + bodies['about'])

# ── CTA (unnumbered section) ──
cta_section = f'''
        <section>
{bodies['cta']}
        </section>

'''

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ASSEMBLE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

final = header + sec01 + sec02 + sec03 + sec04 + sec05 + sec06 + sec07 + cta_section + footer

# FINAL CHECKS
bal = div_balance(final)
print(f'\n━━━ FINAL DOCUMENT ━━━')
print(f'  Total bytes: {len(final)}')
print(f'  Div balance: {bal} {"✅" if bal == 0 else "❌ — FIXING..."}')

if bal != 0:
    # The imbalance comes from section bodies having extra closing divs
    # that originally closed wrapper divs within V12 sections.
    # Fix: count each section body's balance and add compensating opens/closes.
    
    # Actually, the right fix: look at which bodies are imbalanced and patch them
    for name in ['platform', 'hardware', 'fleet']:
        b = div_balance(bodies[name])
        if b < 0:
            # This body has extra </div> tags — these were closing wrapper divs  
            # in V12 that the section-header stripper missed.
            # Add compensating <div> opens at the start.
            print(f"  Patching {name}: {b:+d} (adding {abs(b)} opening divs)")
            bodies[name] = ('<div>\n' * abs(b)) + bodies[name]
    
    # Rebuild with patched bodies
    service_parts_fixed = []
    service_parts_fixed.append('''\
            <p>Augos delivers a fully managed energy intelligence service — not just hardware, not just software, but a unified operational capability purpose-built for multi-site automotive retail.</p>

            <h3 style="margin-top: 40px; margin-bottom: 16px; color: var(--color-primary);">Specialist Retail Intelligence</h3>
''')
    service_parts_fixed.append(bodies['retail'])
    service_parts_fixed.append('''
            <div class="content-card" style="margin: 40px 0; padding: 40px;">
                <h3 style="font-size: 1.5rem; margin-bottom: 12px; letter-spacing: -0.02em;">Intelligence Where It Matters — On the Showroom Floor</h3>
                <p style="margin-bottom: 24px; max-width: 720px; color: var(--color-muted);">The Augos platform delivers real-time energy alerts and AI insights directly to your mobile device. A CFAO dealership principal can review live consumption anomalies, respond to after-hours baseload breaches, and verify resolution — all without leaving the showroom floor.</p>
                <div style="border-radius: 12px; overflow: hidden; box-shadow: var(--shadow);">
                    <img src="dealership_app_hero.jpg" alt="CFAO Dealership Manager viewing Augos energy alerts on mobile" style="width: 100%; display: block; object-fit: cover; max-height: 420px;" />
                </div>
            </div>

            <h3 style="margin-top: 40px; margin-bottom: 16px; color: var(--color-primary);">The Hardware Kit</h3>
''')
    service_parts_fixed.append(bodies['hardware'])
    service_parts_fixed.append('''
            <h3 style="margin-top: 40px; margin-bottom: 16px; color: var(--color-primary);">National Fleet Oversight</h3>
''')
    service_parts_fixed.append(bodies['fleet'])
    
    sec02_fixed = make_section(2, 'The Complete Augos Service', '\n'.join(service_parts_fixed))
    sec03_fixed = make_section(3, 'The Platform Experience', platform_lead + '\n' + bodies['platform'])
    
    final = header + sec01 + sec02_fixed + sec03_fixed + sec04 + sec05 + sec06 + sec07 + cta_section + footer
    
    bal = div_balance(final)
    print(f'  After patch: div balance = {bal} {"✅" if bal == 0 else "❌"}')

with open(OUT, 'w') as f:
    f.write(final)

print(f'\n✅ Written to {OUT}')
print(f'  Sections: {final.count("<section>")}')
print(f'  Lines: {final.count(chr(10))}')
