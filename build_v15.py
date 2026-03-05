import re

def build_v15():
    with open('/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V14.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Version
    html = html.replace('Version: 14.0 (Enterprise)', 'Version: 15.0 (Global Enterprise)')
    html = html.replace('<title>CFAO Mobility - Augos Energy Intelligence</title>', '<title>CFAO Mobility v15 - Augos Energy Intelligence</title>')

    # 2. Update Sidebar Nav Links
    new_nav = """        <ul class="nav-links">
            <li><a href="#executive" class="active"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" /><path d="M3 9h18" /><path d="M9 21V9" /></svg> 01. Strategic Exec</a></li>
            <li><a href="#challenge"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12" /></svg> 02. The Challenge</a></li>
            <li><a href="#platform"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2 ry=2" /><line x1="8" y1="21" x2="16" y2="21" /><line x1="12" y1="17" x2="12" y2="21" /></svg> 03. Platform UI</a></li>
            <li><a href="#credibility"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg> 04. Credibility</a></li>
            <li><a href="#hardware"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" /><line x1="4" y1="22" x2="4" y2="15" /></svg> 05. Hardware Edge</a></li>
            <li><a href="#agent"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"/><path d="M12 12L2.1 7.1"/><path d="M12 12l9.9 4.9"/></svg> 06. Autonomous Agent</a></li>
            <li><a href="#integration"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> 07. ERP Integration</a></li>
            <li><a href="#tariff"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg> 08. Tariff Engine</a></li>
            <li><a href="#esg"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="M3.29 7L12 12l8.71-5"/><path d="M12 22V12"/></svg> 09. ESG & Carbon</a></li>
            <li><a href="#security"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> 10. Multi-Tier Security</a></li>
            <li><a href="#genai"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg> 11. AI Procurement</a></li>
            <li><a href="#hierarchy"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><path d="M8 8l8 8"/><path d="M16 8l-8 8"/></svg> 12. Portfolio Navigation</a></li>
            <li><a href="#alerts"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg> 13. Intelligent Alerts</a></li>
            <li><a href="#whitelabel"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><line x1="12" y1="22" x2="12" y2="12"/></svg> 14. Brand Alignment</a></li>
            <li><a href="#knowledge"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> 15. Training Hub</a></li>
            <li><a href="#financials"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg> 16. Baselines & ROI</a></li>
            <li><a href="#pricing"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg> 17. Commercial Pricing</a></li>
            <li><a href="#deployment"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg> 18. Roll-out Plan</a></li>
        </ul>"""
    
    # regex sub for nav links
    html = re.sub(r'<ul class="nav-links">.*?</ul>', new_nav, html, flags=re.DOTALL)

    # 3. New Sections HTML
    new_sections = """

        <!-- SECTION 06: AUTONOMOUS AGENT -->
        <section id="agent" class="section">
            <div class="glow-orb-2"></div>
            <div class="section-header">
                <span class="section-number">06</span>
                <h2 class="section-title">The Autonomous Energy Manager &amp; ADK</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                Traditional analytics require experts to mine for data. The Augos Agentic Development Kit (ADK) introduces an automated digital worker that actively monitors your portfolio, resolving queries in natural language.
            </p>
            <div class="ui-mockup" style="background: rgba(15, 23, 42, 0.8);">
                <div class="ui-header" style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <div class="ui-dot" style="background:#EF4444"></div>
                    <div class="ui-dot" style="background:#F59E0B"></div>
                    <div class="ui-dot" style="background:#10B981"></div>
                    <div class="ui-title">augos.io / intelligence / adk</div>
                </div>
                <div style="padding: 24px;">
                    <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                        <strong style="color:white; display:block; margin-bottom:8px;">You:</strong>
                        <span style="color:var(--text-muted); font-size: 0.95rem;">"Which of our KZN dealerships breached their after-hours baseload this weekend?"</span>
                    </div>
                    <div style="background: rgba(36, 99, 235, 0.1); border-left: 2px solid var(--primary); border-radius: 8px; padding: 16px;">
                        <strong style="color:var(--primary); display:block; margin-bottom:8px;">Augos HiveMind:</strong>
                        <span style="color:white; font-size: 0.95rem; line-height: 1.6;">I analyzed the 14 sites in KZN. <strong>CFAO Toyota Pinetown</strong> exceeded its 1.2kW baseline, drawing an average of 4.5kW from Friday 6PM to Monday 6AM due to the showroom AC remaining active. This 212 kWh waste cost approximately R760.<br><br>I have already dispatched a Level 1 alert to the Regional Manager via the internal protocol.</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- SECTION 07: ERP INTEGRATION -->
        <section id="integration" class="section">
            <div class="section-header">
                <span class="section-number">07</span>
                <h2 class="section-title">Financial Systems &amp; API Integrations</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                Energy is inherently financial. Built with modern, GraphQL & REST APIs, Augos bridges the operational and financial gap by pushing verified usage telemetry directly into Xero, Power BI, and legacy ERP suites. 
            </p>
            <div class="grid-3">
                <div class="feature-card">
                    <h4 style="color:white; margin-bottom:12px;">Automated Ledger Flow</h4>
                    <p style="font-size: 0.9rem; color: var(--text-muted);">Eliminate manual journaling. Energy costs are programmatically inserted into nominal ledger codes per dealership directly via the Xero/ERP API.</p>
                </div>
                <div class="feature-card">
                    <h4 style="color:white; margin-bottom:12px;">Real-Time Power BI Feed</h4>
                    <p style="font-size: 0.9rem; color: var(--text-muted);">The Augos Azure/GCP connector securely pipes processed, normalized data instantly into the executive team's existing Power BI data lakes.</p>
                </div>
                <div class="feature-card">
                    <h4 style="color:white; margin-bottom:12px;">Tenant Sub-Billing</h4>
                    <p style="font-size: 0.9rem; color: var(--text-muted);">Automatically generate verifiable, branded invoices for any standalone tenants or secondary entities sharing a bulk connection.</p>
                </div>
            </div>
        </section>

        <!-- SECTION 08: TARIFF ENGINE -->
        <section id="tariff" class="section">
            <div class="section-header">
                <span class="section-number">08</span>
                <h2 class="section-title">Advanced Tariff &amp; Bill Verification Engine</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                Municipalities frequently overcharge. Augos digitizes complex Eskom and Municipal tariff schemes (Time-of-Use, Seasonal, Maximum Demand charges) to programmatically audit incoming utility bills line-by-line.
            </p>
            <div style="display:flex; gap:20px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); padding: 24px; border-radius: 12px;">
                    <div style="font-size: 0.85rem; color: var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">City of Tshwane Bill</div>
                    <div style="font-size: 2rem; font-weight:700; color:white; margin-bottom: 8px;">R 142,504.00</div>
                    <div style="color:var(--text-muted); font-size:0.9rem;">Period: Jan 2026</div>
                </div>
                <div style="flex: 1; min-width: 300px; background: rgba(16, 185, 129, 0.05); border: 1px solid var(--success); padding: 24px; border-radius: 12px;">
                    <div style="font-size: 0.85rem; color: var(--success); text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Augos Shadow Calculation</div>
                    <div style="font-size: 2rem; font-weight:700; color:var(--success); margin-bottom: 8px;">R 128,150.25</div>
                    <div style="color:white; font-size:0.9rem; margin-top:12px; border-top: 1px solid rgba(16,185,129,0.2); padding-top:12px;">
                        <strong>Discrepancy: R14,353.75</strong><br>
                        <span style="color: #94a3b8;">Erroneous 130kVA Network Demand Charge applied during off-peak window. Dispute PDF automatically generated.</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- SECTION 09: ESG -->
        <section id="esg" class="section">
            <div class="section-header">
                <span class="section-number">09</span>
                <h2 class="section-title">Automated ESG &amp; Scope 2 Carbon Reporting</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                With tightening corporate governance and compliance frameworks, Augos natively converts exact kWh telemetry into scientifically-backed Scope 2 emissions matrices required for corporate ESG disclosures.
            </p>
            <div class="grid-2">
                <div class="feature-card">
                    <div style="font-size: 3rem; font-weight:800; color:white; margin-bottom:12px;">24,500 <span style="font-size: 1.2rem; color:var(--text-muted); font-weight:400;">tCO2e</span></div>
                    <div style="font-weight: 600; color:var(--primary); margin-bottom: 8px;">Automated GHG Protocol Integration</div>
                    <p style="color:var(--text-muted); font-size:0.9rem;">Applies localized grid emission factors (e.g., Eskom 1.04kg/kWh) instantly.</p>
                </div>
                <div class="feature-card">
                    <div style="font-size: 3rem; font-weight:800; color:white; margin-bottom:12px;">Zero <span style="font-size: 1.2rem; color:var(--text-muted); font-weight:400;">Spreadsheets</span></div>
                    <div style="font-weight: 600; color:var(--primary); margin-bottom: 8px;">Board-Ready Export</div>
                    <p style="color:var(--text-muted); font-size:0.9rem;">One-click PDF/CSV reports structured for Tier-1 corporate auditors and annual ESG reports.</p>
                </div>
            </div>
        </section>

        <!-- SECTION 10: SECURITY -->
        <section id="security" class="section">
            <div class="section-header">
                <span class="section-number">10</span>
                <h2 class="section-title">Multi-Tiered Security &amp; Access Graph</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                Architected on Google Cloud with zero-trust principles. CFAO dictates precisely what data flows where, utilizing our proprietary "Access Graph" to align user permissions with operational hierarchies.
            </p>
            <ul style="list-style:none; padding:0; display:flex; flex-direction:column; gap:16px;">
                <li style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); padding: 16px; border-radius: 8px; display:flex; align-items:center; gap:16px;">
                    <div style="width: 40px; height: 40px; border-radius: 8px; background: rgba(59,130,246,0.1); display:flex; align-items:center; justify-content:center; color:var(--primary);"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
                    <div><strong style="color:white; display:block; font-size:1rem;">End-to-End Encryption</strong><span style="color:var(--text-muted); font-size:0.85rem;">AES-256 data at rest and TLS 1.3 telemetry streaming.</span></div>
                </li>
                <li style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); padding: 16px; border-radius: 8px; display:flex; align-items:center; gap:16px;">
                    <div style="width: 40px; height: 40px; border-radius: 8px; background: rgba(59,130,246,0.1); display:flex; align-items:center; justify-content:center; color:var(--primary);"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><circle cx="6" cy="6" r="3"/><circle cx="18" cy="18" r="3"/><path d="M8 8l8 8"/></svg></div>
                    <div><strong style="color:white; display:block; font-size:1rem;">Granular IAM Model</strong><span style="color:var(--text-muted); font-size:0.85rem;">Regional Managers only see their provinces; Dealer Principals only see their specific branch.</span></div>
                </li>
                <li style="background: rgba(255,255,255,0.03); border: 1px solid var(--border); padding: 16px; border-radius: 8px; display:flex; align-items:center; gap:16px;">
                    <div style="width: 40px; height: 40px; border-radius: 8px; background: rgba(59,130,246,0.1); display:flex; align-items:center; justify-content:center; color:var(--primary);"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></div>
                    <div><strong style="color:white; display:block; font-size:1rem;">POPIA Data Residency</strong><span style="color:var(--text-muted); font-size:0.85rem;">All financial and consumption datasets localized and secured for full framework compliance.</span></div>
                </li>
            </ul>
        </section>

        <!-- SECTION 11: AI PROCUREMENT -->
        <section id="genai" class="section">
            <div class="section-header">
                <span class="section-number">11</span>
                <h2 class="section-title">Generative AI Procurement Analysis</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                CFAO's scale means evaluating dozens of Solar PPA and renewable vendor contracts constantly. Augos utilizes Vertex AI to rapidly ingest rigid vendor proposals and cross-reference them against empirical site data to validate the ROI.
            </p>
            <div class="feature-card" style="border-left: 4px solid #8b5cf6;">
                <h3 style="color:#8b5cf6; margin-bottom:8px; font-size: 1.1rem;">AI Procurement Audit: Vendor B (Solar PPA)</h3>
                <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;"><strong>Result: Rejected/Renegotiate.</strong> The vendor's yield forecast promises 450 kWh per day and a 10% saving based on an assumed blended rate of R3.80. However, our empirical site load profiles prove that 40% of generation will fall on weekends during low dealership baseload. Without battery storage, clipping will ruin the ROI. We recommend rejecting this PPA structure.</p>
                <div style="font-size:0.8rem; color:#666; font-family: 'JetBrains Mono', monospace;">Analysis processed natively via Vertex AI Model: Gem-1.5-Pro</div>
            </div>
        </section>

        <!-- SECTION 12: PORTFOLIO NAVIGATION -->
        <section id="hierarchy" class="section" style="position: relative;">
            <div class="glow-orb"></div>
            <div class="section-header">
                <span class="section-number">12</span>
                <h2 class="section-title">Interactive Portfolio Navigation</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                Managing 100+ sites is impossible with flat spreadsheets. The Augos platform renders interactive hierarchy trees and geospatial map views, allowing C-Suite executives to glide from a national macro-view down to a specific distribution board in three clicks.
            </p>
            <div class="ui-mockup" style="padding: 0; background: transparent; border: none; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);">
                <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid var(--border); border-radius: 12px; padding: 24px;">
                    <h4 style="color:white; margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 12px;">Operating Hierarchy: South Africa</h4>
                    <div style="padding-left: 16px; border-left: 2px solid var(--primary); margin-left: 8px;">
                        <strong style="color:white; display:block; margin-bottom:8px; display:flex; align-items:center; gap:8px;"><span style="color:var(--primary);">▼</span> CFAO Mobility (National Holdings)</strong>
                        
                        <div style="padding-left: 24px; border-left: 2px solid rgba(255,255,255,0.1); margin-left: 8px; margin-top:12px;">
                            <strong style="color:white; display:block; margin-bottom:8px; display:flex; align-items:center; gap:8px;"><span style="color:var(--primary);">▼</span> Western Cape Region</strong>
                            
                            <div style="padding-left: 24px; margin-left: 8px; margin-top:12px;">
                                <div style="display:flex; justify-content:space-between; align-items:center; background: rgba(255,255,255,0.05); padding: 8px 16px; border-radius: 6px; margin-bottom:6px; cursor:pointer;">
                                    <span style="color:var(--text-muted);">CFAO VW Claremont</span>
                                    <span class="pill" style="background: rgba(16, 185, 129, 0.1); color: var(--success);">Optimal</span>
                                </div>
                                <div style="display:flex; justify-content:space-between; align-items:center; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 8px 16px; border-radius: 6px; margin-bottom:6px; cursor:pointer;">
                                    <span style="color:white;">CFAO Toyota Tygervalley</span>
                                    <span class="pill danger" style="background: rgba(239, 68, 68, 0.2); color: var(--danger);">Critical Alert</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- SECTION 13: ALERTS -->
        <section id="alerts" class="section">
            <div class="section-header">
                <span class="section-number">13</span>
                <h2 class="section-title">The Intelligent Alert Feed (Noise Reduction)</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                Traditional platforms overwhelm staff with raw data notifications. Augos employs statistical anomaly detection to learn a specific dealership's "normal" rhythm, severely filtering the noise. You only receive alerts that are financially or structurally significant.
            </p>
            <div style="display:grid; gap:12px;">
                <div style="display:flex; align-items:center; gap:16px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 16px; border-radius: 8px;">
                     <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--danger); box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);"></div>
                     <div style="flex:1;">
                        <strong style="color:white; display:block;">P1 Critical: Phase Imbalance</strong>
                        <span style="color:var(--text-muted); font-size:0.9rem;">Phase 2 voltage dropped 18% below nominal for >5 minutes. Compressor motor damage imminent.</span>
                     </div>
                     <div style="color:#666; font-size:0.8rem; font-family:'JetBrains Mono', monospace;">TRIGGERED</div>
                </div>
                <div style="display:flex; align-items:center; gap:16px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 16px; border-radius: 8px;">
                     <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--warning); box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);"></div>
                     <div style="flex:1;">
                        <strong style="color:white; display:block;">P2 Anomaly: Weekend Baseload</strong>
                        <span style="color:var(--text-muted); font-size:0.9rem;">Site load locked at 8kW Sunday 9AM. Expected 1.5kW. Suspected faulty HVAC timer.</span>
                     </div>
                     <div style="color:var(--success); font-size:0.8rem; font-family:'JetBrains Mono', monospace;">RESOLVED</div>
                </div>
            </div>
        </section>

        <!-- SECTION 14: WHITE-LABELING -->
        <section id="whitelabel" class="section">
            <div class="section-header">
                <span class="section-number">14</span>
                <h2 class="section-title">White-Labeling &amp; Brand Alignment</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                CFAO isn't just buying SaaS—it's establishing an internal capability. The Intelligence platform can be reskinned with your exact corporate colorways, logos, and custom SVG iconography, transforming the platform into a proprietary internal asset (e.g., CFAO Energy Intelligence).
            </p>
            <div class="grid-3">
                <div style="border: 1px dashed rgba(255,255,255,0.2); padding: 24px; text-align: center; border-radius: 8px;">
                    <div style="width: 48px; height: 48px; background: white; border-radius: 50%; margin: 0 auto 16px;"></div>
                    <strong style="color:white; font-size:0.9rem;">Custom Dark/Light Themes</strong>
                </div>
                <div style="border: 1px dashed rgba(255,255,255,0.2); padding: 24px; text-align: center; border-radius: 8px;">
                    <div style="width: 48px; height: 48px; background: var(--primary); border-radius: 50%; margin: 0 auto 16px;"></div>
                    <strong style="color:white; font-size:0.9rem;">Brand Accent Colors</strong>
                </div>
                <div style="border: 1px dashed rgba(255,255,255,0.2); padding: 24px; text-align: center; border-radius: 8px;">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:var(--text-muted); margin: 0 auto 16px;"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
                    <strong style="color:white; font-size:0.9rem; display:block;">Custom Domain / URL</strong>
                </div>
            </div>
        </section>

        <!-- SECTION 15: KNOWLEDGE HUB -->
        <section id="knowledge" class="section">
            <div class="section-header">
                <span class="section-number">15</span>
                <h2 class="section-title">Automated Knowledge &amp; Training Hub</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                Enterprise deployments fail when staff don't understand the data. Augos ships with an integrated, dynamically updating Knowledge Base—featuring rich articles on cost-breakdowns, interactive glossaries, and structural guidance customized to CFAO's infrastructure context.
            </p>
            <div class="feature-card" style="padding: 24px; display:flex; align-items:center; gap: 24px;">
                <div style="width: 64px; height: 64px; border-radius: 12px; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); display:flex; align-items:center; justify-content:center; color: var(--success); flex-shrink:0;">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                </div>
                <div>
                    <h4 style="color:white; margin-bottom:8px; font-size:1.1rem;">In-Context Learning</h4>
                    <p style="font-size:0.9rem; color:var(--text-muted);">Users can hover over any complex metric (e.g. 'Network Demand Charge' or 'Reactive Energy') to instantly pop-up the associated internal KB documentation, drastically reducing the training barrier for non-engineers.</p>
                </div>
            </div>
        </section>

"""
    # 4. Inject 10 New Sections before Section 06
    html = html.replace('<!-- SECTION 06: FINANCIALS & ROI -->', new_sections + '\n        <!-- SECTION 16: FINANCIALS & ROI -->')
    
    # Update Section Headers for 16, 17, 18
    html = html.replace('<section id="financials" class="section">\n            <div class="section-header">\n                <span class="section-number">06</span>', '<section id="financials" class="section">\n            <div class="section-header">\n                <span class="section-number">16</span>')
    html = html.replace('<section id="deployment" class="section" style="border-bottom: none;">\n            <div class="section-header">\n                <span class="section-number">07</span>', '<section id="deployment" class="section" style="border-bottom: none;">\n            <div class="section-header">\n                <span class="section-number">18</span>')
    
    # 5. Add New Pricing Section before Deployment Strategy
    new_pricing = """

        <!-- SECTION 17: PRICING -->
        <section id="pricing" class="section">
            <div class="section-header">
                <span class="section-number">17</span>
                <h2 class="section-title">Enterprise Commercials &amp; SaaS Models</h2>
            </div>
            <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px; margin-bottom: 40px;">
                Flexible commercial structures designed around OPEX optimization. Choose immediate capital acquisition or a fully managed Hardware-as-a-Service (HaaS) subscription across the entire multi-site portfolio.
            </p>
            
            <div class="grid-2">
                <div class="feature-card" style="border: 1px solid var(--border);">
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
            
        </section>

"""

    html = html.replace('<!-- SECTION 18: DEPLOYMENT -->', '<!-- SECTION 18: DEPLOYMENT -->') # no-op just logic placeholder
    # Actually wait, V14 had <!-- SECTION 07: DEPLOYMENT --> , I replaced 07 with 18.
    html = html.replace('<!-- SECTION 07: DEPLOYMENT -->', new_pricing + '<!-- SECTION 18: DEPLOYMENT -->')
    

    with open('/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V15.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
if __name__ == '__main__':
    build_v15()
