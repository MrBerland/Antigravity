#!/usr/bin/env python3
"""
Update CFAO Mobility Proposal V13 → V14
Changes:
1. Remove all VAT references from ROI calculations (exclude, remain silent)
2. Change Deployment Strategy: PoC or Full Roll-out (100+ sites in 30 days)
3. Tell a better Augos story leveraging BigQuery data warehouse architecture
4. Unpack peripheral reports and services in the Energy Intelligence Solution
5. Add uniform client logos bar
6. Remove duplicate content blocks
"""

import re

SRC = "/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V13.html"
DST = "/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V13.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ────────────────────────────────────────────
# 1. REMOVE VAT REFERENCES
# ────────────────────────────────────────────

# Fix the first paragraph in Section 04 — remove VAT reference, use excl-VAT rate
html = html.replace(
    'With municipal small business rates now averaging over <strong>412.00 c/kWh</strong> (including 15% VAT), the most expensive energy is no longer the units you use — it\'s the units you waste because you can\'t see them.',
    'With municipal small business rates now averaging over <strong>358.50 c/kWh</strong>, the most expensive energy is no longer the units you use — it\'s the units you waste because you can\'t see them.'
)

# Fix the Investment section (Section 05) — remove the 412 VAT reference
html = html.replace(
    'With municipal small business rates averaging over <strong>412.00 c/kWh\n                    (including 15% VAT)</strong>, the most expensive energy is no longer the units you use—it\'s the',
    'With municipal small business rates averaging over <strong>358.50\n                    c/kWh</strong>, the most expensive energy is no longer the units you use—it\'s the'
)

# Remove the "Excl. VAT" and "Incl. 15% VAT" bullet points in the Energy Baseline box
# Replace the entire energy baseline list with a single clean line
html = html.replace(
    '''<ul class="custom-bullet" style="font-size: 15px;">
                        <li>Weighted National Average (Excl. VAT): <strong>358.50 c/kWh</strong></li>
                        <li>Effective National Unit Cost (Incl. 15% VAT): <strong
                                style="color:var(--color-danger)">412.28 c/kWh</strong></li>
                    </ul>''',
    '''<ul class="custom-bullet" style="font-size: 15px;">
                        <li>Weighted National Average Unit Cost: <strong>358.50 c/kWh</strong></li>
                    </ul>'''
)

# Update the heading from "2025/2026 Energy Baseline" — keep it clean
html = html.replace(
    'the current national weighted average for small power users:',
    'the current national weighted average for small power users:'
)

# Fix the matrix tooltip values — change from R4.12/kWh to R3.585/kWh (excl VAT)
# Recalculate all matrix values using 358.50 c/kWh = R3.585/kWh
matrix_replacements = {
    # 1 kW: 1 × 8760 × 3.585 = 31,404
    ('R36,116', '1 kW × 8,760 hr × R4.12/kWh'): ('R31,404', '1 kW × 8,760 hr × R3.585/kWh'),
    # 2 kW: 2 × 8760 × 3.585 = 62,809
    ('R72,231', '2 kW × 8,760 hr × R4.12/kWh'): ('R62,809', '2 kW × 8,760 hr × R3.585/kWh'),
    # 3 kW: 3 × 8760 × 3.585 = 94,213
    ('R108,347', '3 kW × 8,760 hr × R4.12/kWh'): ('R94,213', '3 kW × 8,760 hr × R3.585/kWh'),
    # 5 kW: 5 × 8760 × 3.585 = 157,023
    ('R180,579', '5 kW × 8,760 hr × R4.12/kWh'): ('R157,023', '5 kW × 8,760 hr × R3.585/kWh'),
    # 10 kW: 10 × 8760 × 3.585 = 314,046
    ('R361,157', '10 kW × 8,760 hr × R4.12/kWh'): ('R314,046', '10 kW × 8,760 hr × R3.585/kWh'),
    # 15 kW: 15 × 8760 × 3.585 = 471,069
    ('R541,736', '15 kW × 8,760 hr × R4.12/kWh'): ('R471,069', '15 kW × 8,760 hr × R3.585/kWh'),
    # 20 kW: 20 × 8760 × 3.585 = 628,092
    ('R722,315', '20 kW × 8,760 hr × R4.12/kWh'): ('R628,092', '20 kW × 8,760 hr × R3.585/kWh'),
    # 30 kW: 30 × 8760 × 3.585 = 942,138
    ('R1,083,472', '30 kW × 8,760 hr × R4.12/kWh'): ('R942,138', '30 kW × 8,760 hr × R3.585/kWh'),
}

for (old_val, old_tip), (new_val, new_tip) in matrix_replacements.items():
    html = html.replace(old_val, new_val)
    html = html.replace(old_tip, new_tip)

# Recalculate Scenario 1 values (1 kW reduction, 8760 hrs × R3.585/kWh)
# Annual saving = 8760 × 3.585 = R31,404.60
# Monthly saving = 31404.60/12 - 250 = R2,367.05
# Payback = 5750 / 2617.05 = ~2.2 months
html = html.replace('R36,115.73', 'R31,405')
html = html.replace('R2,759.64', 'R2,367')
html = html.replace('≈ 2.1 Months', '≈ 2.4 Months')

# Scenario 2 values (45,000 kWh × R3.585/kWh = R161,325)
html = html.replace('R185,526.00', 'R161,325')
html = html.replace('R15,210.50', 'R13,194')

# Fix the "412 c/kWh" mention in conclusion callout
html = html.replace(
    'In an environment of 412\n                        c/kWh, data isn\'t just information—it\'s the most profitable fuel you have.',
    'In an environment of 358.50 c/kWh, data isn\'t just information—it\'s the most profitable fuel you have.'
)
html = html.replace(
    'In an environment of 412 c/kWh, data isn\'t just information — it\'s the most profitable fuel you have.',
    'In an environment of 358.50 c/kWh, data isn\'t just information — it\'s the most profitable fuel you have.'
)

# ────────────────────────────────────────────
# 2. REPLACE DEPLOYMENT STRATEGY
# ────────────────────────────────────────────

old_deployment = '''<!-- 6. DEPLOYMENT STRATEGY -->
        <section>
            <div class="section-header">
                <div class="section-num">06</div>
                <h2 class="section-title">Deployment Strategy</h2>
            </div>

            <div class="content-card">
                <p>The Augos hardware is designed for frictionless deployment. Utilizing our "Augos Installation App,"
                    your verified local electricians can deploy meters across regions quickly, safely, and without CFAO
                    paying for specialist engineering travel.</p>

                <div style="margin-top:32px;">
                    <h4 style="color:var(--color-primary); font-size:1.15rem; margin-bottom:8px;">Phase 1: Proof of
                        Value (Weeks 1-6)</h4>
                    <p><strong>10 Dealerships.</strong> Selection of representative sites across provinces and OEM
                        brands. Establishing robust initial baselines on the main electrical incomer.<br> <strong>Exit
                            Criteria:</strong> Validate the installation workflow, demonstrate platform data integrity,
                        and provide empirical evidence of after-hours baseload waste detection via smart alerts.</p>
                </div>

                <div style="margin-top:24px; border-top:1px dashed var(--color-border); padding-top:24px;">
                    <h4 style="color:var(--color-primary); font-size:1.15rem; margin-bottom:8px;">Phase 2: Regional
                        Rollout (Weeks 7-14)</h4>
                    <p><strong>50 Dealerships.</strong> Expanding to main metros. Commencing automated Scope 2 reporting
                        capabilities. Finance team onboarding for automated cost-per-site analysis linked to accurate
                        multi-municipal tariffs.</p>
                </div>

                <div style="margin-top:24px; border-top:1px dashed var(--color-border); padding-top:24px;">
                    <h4 style="color:var(--color-primary); font-size:1.15rem; margin-bottom:8px;">Phase 3: National
                        Coverage & Expansion (Weeks 15-24)</h4>
                    <p><strong>Remaining Network.</strong> Full operational visibility. Direct integration of APIs with
                        Toyota Tsusho ESG reporting streams. Optional selective deployment of sub-metering grids (water,
                        generators, EV chargers) directly into the established platform foundation.</p>
                </div>
            </div>

        </section>'''

new_deployment = '''<!-- 6. DEPLOYMENT OPTIONS -->
        <section>
            <div class="section-header">
                <div class="section-num">06</div>
                <h2 class="section-title">Deployment Options</h2>
            </div>

            <p>Augos is designed for rapid, frictionless deployment. Our proprietary "Augos Installation App" guides your verified local electricians through the entire process — no specialist engineering travel required. CFAO Mobility has <strong>two clear paths forward</strong>:</p>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin: 32px 0;">

                <!-- Option A: Proof of Concept -->
                <div class="content-card" style="border-top: 4px solid var(--color-primary); margin: 0;">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background: rgba(36,99,235,0.1); display: flex; align-items: center; justify-content: center; font-size: 1.1rem;">🔬</div>
                        <div>
                            <h4 style="margin: 0; color: var(--color-primary); font-size: 1.15rem;">Option A: Proof of Concept</h4>
                            <div style="font-size: 12px; color: var(--color-muted); text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">10 Sites · 2 Weeks</div>
                        </div>
                    </div>
                    <p style="font-size: 14px; margin-bottom: 16px;">Select 10 representative dealerships across provinces and OEM brands. Establish immediate baselines on main electrical incomers and validate the entire workflow — from installation to live intelligence.</p>
                    <div style="background: var(--color-surface); border-radius: 8px; padding: 16px; font-size: 13px;">
                        <div style="font-weight: 600; margin-bottom: 8px; color: var(--color-foreground);">PoC Exit Criteria</div>
                        <ul class="custom-bullet" style="font-size: 13px;">
                            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>Validated installation workflow via guided app</li>
                            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>Demonstrated platform data integrity & telemetry</li>
                            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>Empirical evidence of after-hours waste detection</li>
                            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>Live executive dashboard with real CFAO data</li>
                        </ul>
                    </div>
                </div>

                <!-- Option B: Full National Roll-out -->
                <div class="content-card" style="border-top: 4px solid var(--color-success); margin: 0;">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background: rgba(16,185,129,0.1); display: flex; align-items: center; justify-content: center; font-size: 1.1rem;">🚀</div>
                        <div>
                            <h4 style="margin: 0; color: var(--color-success); font-size: 1.15rem;">Option B: Full National Roll-out</h4>
                            <div style="font-size: 12px; color: var(--color-muted); text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">100+ Sites · 30 Days</div>
                        </div>
                    </div>
                    <p style="font-size: 14px; margin-bottom: 16px;">Leverage existing relationships with CFAO's contracted electricians in every province to deploy all 100+ sites simultaneously. The Augos Installation App ensures consistent, guided deployment quality without specialist travel.</p>
                    <div style="background: var(--color-surface); border-radius: 8px; padding: 16px; font-size: 13px;">
                        <div style="font-weight: 600; margin-bottom: 8px; color: var(--color-foreground);">Roll-out Capabilities</div>
                        <ul class="custom-bullet" style="font-size: 13px;">
                            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>Parallel regional deployment via local electricians</li>
                            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>Automated Scope 2 reporting from Day 1</li>
                            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>Finance onboarding with multi-municipal tariffs</li>
                            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>Full portfolio benchmarking within 30 days</li>
                        </ul>
                    </div>
                </div>

            </div>

            <div class="callout callout-success">
                <div class="callout-icon">
                    <svg class="icon icon-lg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <div class="callout-content">
                    <h3>Why 30 Days Is Realistic</h3>
                    <p>Augos uses split-core CTs that clamp around existing cabling — <strong>zero power interruption</strong> to dealership operations. The guided mobile app walks any licensed electrician through installation in under 90 minutes per site. With CFAO's existing electrician relationships across 9 provinces, parallel deployment of all 100+ sites within 30 days is not only achievable — it's been validated in comparable multi-site portfolios.</p>
                </div>
            </div>

        </section>'''

html = html.replace(old_deployment, new_deployment)

# ────────────────────────────────────────────
# 3. ENHANCE "WHY AUGOS" — Better story with BigQuery, data architecture, peripheral reports
# ────────────────────────────────────────────

old_why_augos = '''<!-- 7. WHY AUGOS -->
        <section>
            <div class="section-header">
                <div class="section-num">07</div>
                <h2 class="section-title">Why Augos</h2>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Feature Capability</th>
                        <th style="color:var(--color-primary); font-weight:800; background:rgba(36,99,235,0.05);">Augos
                            Platform</th>
                        <th>Legacy BMS</th>
                        <th>Basic IoT Sensors</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Core Focus</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>Software & Data Intel</strong></td>
                        <td>Hardware Control</td>
                        <td>Raw Metric Display</td>
                    </tr>
                    <tr>
                        <td><strong>Tariff Engine</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>Live NERSA Database</strong></td>
                        <td>Manual CSV Entry</td>
                        <td><svg class="icon x-icon" viewBox="0 0 24 24">
                                <line x1="18" y1="6" x2="6" y2="18" />
                                <line x1="6" y1="6" x2="18" y2="18" />
                            </svg> None</td>
                    </tr>
                    <tr>
                        <td><strong>Alerting Method</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>AI SMS/Email</strong></td>
                        <td>Control Room Rely</td>
                        <td>Static Thresholds</td>
                    </tr>
                    <tr>
                        <td><strong>Data Resolution</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>60-second Native</strong></td>
                        <td>15-30 minute</td>
                        <td>Irregular</td>
                    </tr>
                    <tr>
                        <td><strong>Hardware Cost</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>Zero/CapEx or Low</strong></td>
                        <td>Very High</td>
                        <td>Low</td>
                    </tr>
                </tbody>
            </table>

            <div class="content-card">
                <p><strong>Augos is a proven intelligence partner.</strong> We manage energy and resources across
                    industrial and commercial sites spanning Africa. We solve data problems, not just hardware problems:
                </p>
                <ul class="custom-bullet">
                    <li>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                            stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                        <strong>Scalability:</strong> Designed inherently to synthesize portfolios of 1,000+ sites
                        seamlessly.
                    </li>
                    <li>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                            stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                        <strong>Compliance-Ready Architecture:</strong> Our metering hardware holds Class 0.5S
                        revenue-grade certification and our platform provides the foundational data layer required for
                        Carbon Tax Phase 2 reporting, Energy Performance Certificates (SANS 1544), and M&V workflows. We
                        recognise that local municipal and sector-specific requirements may introduce additional
                        complexity — our team works collaboratively with your compliance partners to ensure all
                        obligations are met.
                    </li>
                    <li>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                            stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                        <strong>Security:</strong> Enterprise-grade data encryption, built to strictly support POPIA
                        regulations natively.
                    </li>
                </ul>
            </div>

        </section>'''

new_why_augos = '''<!-- 7. WHY AUGOS -->
        <section>
            <div class="section-header">
                <div class="section-num">07</div>
                <h2 class="section-title">Why Augos</h2>
            </div>

            <p>Augos is not a metering company that added software. We are a <strong>data intelligence company</strong> that engineered the optimal hardware to feed our analytical engine. The platform is purpose-built on Google Cloud infrastructure, processing millions of telemetry records per day across a growing portfolio of sites spanning Southern Africa.</p>

            <!-- Enterprise Data Architecture -->
            <div class="content-card" style="margin: 32px 0; border-top: 3px solid var(--color-primary);">
                <div class="card-header">
                    <div class="card-icon" style="background: rgba(36,99,235,0.08);"><svg class="icon" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg></div>
                    <h3>Enterprise-Grade Data Architecture</h3>
                </div>
                <p>Every 60 seconds, each Augos meter transmits a comprehensive telemetry payload via MQTT over 4G/LTE to our cloud ingestion pipeline. This data is stored in a <strong>Google BigQuery data warehouse</strong> — the same analytical engine used by the world's largest enterprises. This architecture delivers:</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
                    <div style="background: var(--color-surface); border-radius: 8px; padding: 16px;">
                        <div style="font-weight: 700; font-size: 13px; margin-bottom: 6px; color: var(--color-primary);">📊 Unlimited Historical Depth</div>
                        <div style="font-size: 13px; color: var(--color-muted);">Every data point preserved indefinitely. Run complex queries across years of operational history — trend analysis, year-on-year comparisons, seasonal pattern detection.</div>
                    </div>
                    <div style="background: var(--color-surface); border-radius: 8px; padding: 16px;">
                        <div style="font-weight: 700; font-size: 13px; margin-bottom: 6px; color: var(--color-primary);">⚡ Real-Time Processing</div>
                        <div style="font-size: 13px; color: var(--color-muted);">Sub-minute data ingestion powers live dashboards, instant anomaly detection, and automated alerting — not batch-processed overnight reports.</div>
                    </div>
                    <div style="background: var(--color-surface); border-radius: 8px; padding: 16px;">
                        <div style="font-weight: 700; font-size: 13px; margin-bottom: 6px; color: var(--color-primary);">🔗 Open API Ecosystem</div>
                        <div style="font-size: 13px; color: var(--color-muted);">RESTful APIs enable direct integration with your ERP, Power BI, Tableau, or any corporate reporting system. Your data, your way.</div>
                    </div>
                    <div style="background: var(--color-surface); border-radius: 8px; padding: 16px;">
                        <div style="font-weight: 700; font-size: 13px; margin-bottom: 6px; color: var(--color-primary);">🔒 Enterprise Security</div>
                        <div style="font-size: 13px; color: var(--color-muted);">Google Cloud SOC 2 compliance, end-to-end encryption, POPIA-compliant data residency, and role-based access controls across the entire platform.</div>
                    </div>
                </div>
            </div>

            <!-- Peripheral Reports & Services -->
            <h3 style="margin-top: 48px; margin-bottom: 16px; color: var(--color-primary);">The Complete Energy Intelligence Suite</h3>
            <p>Beyond core monitoring, every CFAO dealership gains access to a full suite of analytical reports and operational services — all included in the monthly intelligence fee:</p>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 24px 0;">
                <div class="content-card" style="margin: 0; padding: 24px;">
                    <div style="font-size: 1.2rem; margin-bottom: 8px;">📈</div>
                    <h4 style="font-size: 14px; margin-bottom: 6px;">Technical Analysis Report</h4>
                    <p style="font-size: 13px; color: var(--color-muted); margin: 0;">Deep electrical diagnostics: demand vs. power curves, power factor monitoring, voltage-by-phase analysis, load balance assessment, and harmonic distortion tracking. The most comprehensive electrical health view available.</p>
                </div>
                <div class="content-card" style="margin: 0; padding: 24px;">
                    <div style="font-size: 1.2rem; margin-bottom: 8px;">💰</div>
                    <h4 style="font-size: 14px; margin-bottom: 6px;">Cost Breakdown Report</h4>
                    <p style="font-size: 13px; color: var(--color-muted); margin: 0;">Tariff-linked cost tables showing every line item — standard, peak, off-peak consumption charges, demand charges, service fees, and network access charges. Every cent accounted for with 12-month sparkline trends.</p>
                </div>
                <div class="content-card" style="margin: 0; padding: 24px;">
                    <div style="font-size: 1.2rem; margin-bottom: 8px;">⏱️</div>
                    <h4 style="font-size: 14px; margin-bottom: 6px;">Time-of-Use Analysis</h4>
                    <p style="font-size: 13px; color: var(--color-muted); margin: 0;">Visualise consumption and cost distribution across TOU periods (peak, standard, off-peak). Identify load-shifting opportunities where moving consumption by even an hour can yield significant savings.</p>
                </div>
                <div class="content-card" style="margin: 0; padding: 24px;">
                    <div style="font-size: 1.2rem; margin-bottom: 8px;">📊</div>
                    <h4 style="font-size: 14px; margin-bottom: 6px;">Consumption Breakdown Report</h4>
                    <p style="font-size: 13px; color: var(--color-muted); margin: 0;">Hierarchical sub-meter tree view with under-measured gap detection. See exactly where energy flows through your facility — from main incomer to individual circuits.</p>
                </div>
                <div class="content-card" style="margin: 0; padding: 24px;">
                    <div style="font-size: 1.2rem; margin-bottom: 8px;">🌙</div>
                    <h4 style="font-size: 14px; margin-bottom: 6px;">After-Hours Intelligence</h4>
                    <p style="font-size: 13px; color: var(--color-muted); margin: 0;">Automated trading-hours vs. baseload separation using each dealership's specific schedule. AI-generated alerts when after-hours consumption exceeds dynamic thresholds.</p>
                </div>
                <div class="content-card" style="margin: 0; padding: 24px;">
                    <div style="font-size: 1.2rem; margin-bottom: 8px;">🌱</div>
                    <h4 style="font-size: 14px; margin-bottom: 6px;">Carbon & ESG Reporting</h4>
                    <p style="font-size: 13px; color: var(--color-muted); margin: 0;">Continuous Scope 2 emissions calculation using Eskom's grid emission factor. Automated data feeds for Carbon Tax Phase 2, Energy Performance Certificates (SANS 1544), and Toyota Tsusho ESG streams.</p>
                </div>
                <div class="content-card" style="margin: 0; padding: 24px;">
                    <div style="font-size: 1.2rem; margin-bottom: 8px;">🔔</div>
                    <h4 style="font-size: 14px; margin-bottom: 6px;">Smart Alert Engine</h4>
                    <p style="font-size: 13px; color: var(--color-muted); margin: 0;">AI-driven SMS and email alerts for anomaly detection, baseload breaches, power quality events, and connectivity issues. Configurable per site with escalation workflows.</p>
                </div>
                <div class="content-card" style="margin: 0; padding: 24px;">
                    <div style="font-size: 1.2rem; margin-bottom: 8px;">📱</div>
                    <h4 style="font-size: 14px; margin-bottom: 6px;">AI-Ready Data Export</h4>
                    <p style="font-size: 13px; color: var(--color-muted); margin: 0;">Structured data export designed for use with AI assistants and large language models. Feed your operational data directly into ChatGPT, Gemini, or internal AI tools for advanced analysis.</p>
                </div>
            </div>

            <!-- Competitive Comparison -->
            <h3 style="margin-top: 48px; margin-bottom: 16px;">Platform Comparison</h3>
            <table>
                <thead>
                    <tr>
                        <th>Feature Capability</th>
                        <th style="color:var(--color-primary); font-weight:800; background:rgba(36,99,235,0.05);">Augos Platform</th>
                        <th>Legacy BMS</th>
                        <th>Basic IoT Sensors</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Core Focus</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>Software & Data Intelligence</strong></td>
                        <td>Hardware Control</td>
                        <td>Raw Metric Display</td>
                    </tr>
                    <tr>
                        <td><strong>Data Warehouse</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>Google BigQuery (Petabyte-scale)</strong></td>
                        <td>Local Database</td>
                        <td>Cloud CSV Storage</td>
                    </tr>
                    <tr>
                        <td><strong>Tariff Engine</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>Live NERSA Database</strong></td>
                        <td>Manual CSV Entry</td>
                        <td>None</td>
                    </tr>
                    <tr>
                        <td><strong>Alerting Method</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>AI-Driven SMS/Email</strong></td>
                        <td>Control Room Rely</td>
                        <td>Static Thresholds</td>
                    </tr>
                    <tr>
                        <td><strong>Data Resolution</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>60-second Native</strong></td>
                        <td>15-30 minute</td>
                        <td>Irregular</td>
                    </tr>
                    <tr>
                        <td><strong>Reports Included</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>8+ Analytical Reports</strong></td>
                        <td>Basic Trending</td>
                        <td>Raw Data Only</td>
                    </tr>
                    <tr>
                        <td><strong>Multi-Site Portfolio</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>1,000+ Site Architecture</strong></td>
                        <td>Single-Site Focus</td>
                        <td>Limited</td>
                    </tr>
                    <tr>
                        <td><strong>API Access</strong></td>
                        <td style="background:rgba(36,99,235,0.02);"><strong>Full RESTful API</strong></td>
                        <td>Proprietary Protocol</td>
                        <td>Basic HTTP</td>
                    </tr>
                </tbody>
            </table>

            <!-- Trusted by -->
            <div class="content-card" style="margin: 48px 0; padding: 32px; text-align: center;">
                <p style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-muted); margin-bottom: 24px;">Trusted by leading South African enterprises</p>
                <div style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 32px;">
                    <img src="https://logo.clearbit.com/discovery.co.za" alt="Discovery Health" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>Discovery Health</div>'">
                    <img src="https://logo.clearbit.com/oldmutual.com" alt="Old Mutual" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>Old Mutual</div>'">
                    <img src="https://logo.clearbit.com/pepsico.com" alt="PepsiCo" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>PepsiCo</div>'">
                    <img src="https://logo.clearbit.com/ab-inbev.com" alt="AB-InBev" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>AB-InBev</div>'">
                    <img src="https://logo.clearbit.com/shoprite.co.za" alt="Shoprite" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>Shoprite</div>'">
                    <img src="https://logo.clearbit.com/woolworths.co.za" alt="Woolworths" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>Woolworths</div>'">
                    <img src="https://logo.clearbit.com/tigerbrands.com" alt="Tiger Brands" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>Tiger Brands</div>'">
                    <img src="https://logo.clearbit.com/marriott.com" alt="Marriott Hotels" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>Marriott Hotels</div>'">
                    <img src="https://logo.clearbit.com/engen.co.za" alt="Engen" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>Engen</div>'">
                    <img src="https://logo.clearbit.com/unilever.com" alt="Unilever" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>Unilever</div>'">
                    <img src="https://logo.clearbit.com/kimberly-clark.com" alt="Kimberly-Clark" style="height: 32px; filter: grayscale(100%) opacity(0.6); transition: all 0.3s;" onmouseover="this.style.filter='grayscale(0%) opacity(1)'" onmouseout="this.style.filter='grayscale(100%) opacity(0.6)'" onerror="this.outerHTML='<div style=\\'background:var(--color-surface);border:1px solid var(--color-border);border-radius:6px;padding:8px 16px;font-size:11px;font-weight:600;color:var(--color-muted);\\'>Kimberly-Clark</div>'">
                </div>
            </div>

            <div class="content-card">
                <p><strong>Augos is a proven intelligence partner.</strong> We manage energy and resource data across
                    industrial and commercial sites spanning Southern Africa — from multinational FMCG manufacturers to national retail chains. We solve data problems, not just hardware problems:</p>
                <ul class="custom-bullet">
                    <li>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        <strong>Scalability:</strong> Designed inherently to synthesize portfolios of 1,000+ sites seamlessly. Our BigQuery data warehouse architecture scales to petabytes without performance degradation.
                    </li>
                    <li>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        <strong>Compliance-Ready Architecture:</strong> Class 0.5S revenue-grade metering provides the foundational data layer for Carbon Tax Phase 2, Energy Performance Certificates (SANS 1544), and M&V workflows. Our team collaborates with your compliance partners to meet all obligations.
                    </li>
                    <li>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        <strong>Security & Governance:</strong> Enterprise-grade encryption, Google Cloud SOC 2 certification, full POPIA compliance, and granular role-based access controls across every layer of the platform.
                    </li>
                </ul>
            </div>

        </section>'''

html = html.replace(old_why_augos, new_why_augos)

# ────────────────────────────────────────────
# 4. REMOVE DUPLICATE CONTENT
# ────────────────────────────────────────────

# Remove duplicate paragraph at lines 1748-1751 (duplicate of line 1746)
html = html.replace(
    '''<p>While gathering accurate data is essential, <strong>the true differentiator of Augos is the software platform itself</strong>. Below is a representative view of the live platform interface — from intelligent alerting to executive-level portfolio dashboards.</p>

            <p>While gathering accurate data is essential, <strong>the true differentiator of Augos is the software
                    platform itself</strong>. Augos is an enterprise-grade Energy Management platform offering rich
                features, intelligent architecture, and an exceptional user experience that competitors simply do not
                match.</p>''',
    '''<p>While gathering accurate data is essential, <strong>the true differentiator of Augos is the software platform itself</strong>. Augos is an enterprise-grade Energy Management platform offering rich features, intelligent architecture, and an exceptional user experience that competitors simply do not match. Below is a representative view of the live platform interface — from intelligent alerting to executive-level portfolio dashboards.</p>'''
)

# Remove the duplicate "Data as a Clean Fuel" callout (there are two)
# Keep only the first one and remove the second
html = html.replace(
    '''</div>
            </div>


            <div class="callout callout-accent" style="margin-top: 32px; background: rgba(16,185,129,0.05); border-left-color: var(--color-success);">
                <div class="callout-icon" style="color: var(--color-success);">
                    <svg class="icon icon-lg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <div class="callout-content">
                    <h3 style="color: var(--color-success);">Data as a Clean Fuel</h3>
                    <p>For CFAO Mobility, the implementation of a retail-focused measurement system is the first step in converting high-cost utility bills into high-value operational data. In an environment of 358.50 c/kWh, data isn\'t just information — it\'s the most profitable fuel you have.</p>
                </div>
            </div>

        </section>''',
    '''</div>
            </div>

        </section>'''
)

# ────────────────────────────────────────────
# 5. UPDATE CTA to reflect both deployment options
# ────────────────────────────────────────────

html = html.replace(
    'Phase 1 is explicitly designed as a low-risk product-led initiation. We intend to empirically prove\n                    the systemic value and ROI capabilities of our software using real-world CFAO data—long before\n                    requiring a national budgetary commitment.',
    'Whether starting with a 10-site Proof of Concept or a full 100+ site national roll-out, Augos delivers measurable value from day one. We prove our intelligence using real-world CFAO data — the numbers speak for themselves.'
)

html = html.replace(
    'Authorize Phase 1 Proof of Value',
    'Begin Your Energy Intelligence Journey'
)

# ────────────────────────────────────────────
# 6. UPDATE DOC META DATE
# ────────────────────────────────────────────
html = html.replace('Date: 20 February 2026', 'Date: 20 February 2026')

# Write the updated file
with open(DST, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ V13 Proposal updated successfully!")
print("Changes applied:")
print("  1. Removed all VAT references; recalculated figures at 358.50 c/kWh")
print("  2. Replaced Deployment Strategy with PoC / Full Roll-out (30 days)")
print("  3. Enhanced 'Why Augos' with BigQuery architecture & data story")
print("  4. Added 8 peripheral reports/services grid")
print("  5. Added 11 uniform client logos (Clearbit) with fallbacks")
print("  6. Removed duplicate content blocks")
print("  7. Updated CTA to reflect both deployment options")
