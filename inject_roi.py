import os

in_path = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V10.html'
out_path = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V11.html'

with open(in_path, 'r') as f:
    html = f.read()

css_to_inject = """
        /* Savings Matrix */
        .matrix-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 12px;
            margin-top: 24px;
        }
        .matrix-cell {
            background: #fff;
            border: 1px solid var(--color-border);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            position: relative;
            cursor: default;
            transition: all 0.2s;
            box-shadow: var(--shadow-sm);
        }
        .matrix-cell:hover {
            border-color: var(--color-primary);
            transform: translateY(-2px);
            box-shadow: var(--shadow);
            z-index: 2;
        }
        .matrix-cell .kw-lbl {
            font-size: 13px;
            color: var(--color-muted);
            font-weight: 500;
            margin-bottom: 8px;
        }
        .matrix-cell .val-lbl {
            font-size: 20px;
            font-weight: 700;
            color: var(--color-success);
        }
        .matrix-tooltip {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%) translateY(8px);
            background: #1e293b;
            color: #fff;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 11px;
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: all 0.2s;
            pointer-events: none;
            box-shadow: var(--shadow-lg);
        }
        .matrix-tooltip::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #1e293b transparent transparent transparent;
        }
        .matrix-cell:hover .matrix-tooltip {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(-10px);
        }
        .scenario-box {
            background: var(--color-surface);
            border-left: 4px solid var(--color-primary);
            padding: 24px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 24px;
        }
        .scenario-box h4 {
            font-size: 1.15rem;
            color: var(--color-primary);
            margin-bottom: 12px;
        }
        .scenario-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px dashed var(--color-border);
        }
        .scenario-stat {
            display: flex;
            flex-direction: column;
        }
        .scenario-stat span.lbl { font-size: 12px; color: var(--color-muted); }
        .scenario-stat span.val { font-size: 16px; font-weight: 600; color: var(--color-foreground); }
"""

html = html.replace('</style>', css_to_inject + '\n    </style>')

# Prepare the new section HTML properly
new_roi_section = """
        <!-- 8. INVESTMENT & ROI -->
        <section>
            <div class="section-header">
                <div class="section-num">08</div>
                <h2 class="section-title">Beyond the Hike: The "Survival Kit" for SA Retail</h2>
            </div>
            
            <p>For South African automotive retail and showrooms, the 2025/2026 electricity landscape has moved past a simple "cost of doing business." With municipal small business rates averaging over <strong>412.00 c/kWh (including 15% VAT)</strong>, the most expensive energy is no longer the units you use—it's the units you waste because you can't see them.</p>

            <p>At CFAO Mobility, the path to sustainability isn't just about adding new generation; it's about <strong>Energy Intelligence</strong>: a high-fidelity measurement system that uses benchmarking and critical load signals to turn "dark data" into operational savings.</p>

            <div class="ui-mockup-wrapper" style="padding: 24px; margin-top: 32px; display: grid; grid-template-columns: 1fr 1fr; gap: 40px; border-top: 4px solid var(--color-primary);">
                <div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 16px;">⚡ The 2025/2026 Energy Baseline</h3>
                    <p style="font-size: 14px; color: var(--color-muted); margin-bottom: 16px;">To build an accurate business case, we must use the current national weighted average for small power users:</p>
                    <ul class="custom-bullet" style="font-size: 15px;">
                        <li>Weighted National Average (Excl. VAT): <strong>358.50 c/kWh</strong></li>
                        <li>Effective National Unit Cost (Incl. 15% VAT): <strong style="color:var(--color-danger)">412.28 c/kWh</strong></li>
                    </ul>
                </div>
                <div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 16px;">🛠️ System Investment Breakdown</h3>
                    <p style="font-size: 14px; color: var(--color-muted); margin-bottom: 16px;">The barrier to entry for energy intelligence is exceptionally low compared to the potential savings.</p>
                    <ul class="custom-bullet" style="font-size: 15px;">
                        <li>Total Upfront Capital (Hardware + Comm + Install): <strong>R5,750</strong></li>
                        <li>Monthly Intelligence Fee (SaaS Platform): <strong>R250 / site</strong></li>
                    </ul>
                </div>
            </div>

            <h3 style="margin-top: 48px; margin-bottom: 24px;">The Economics of Intelligence: ROI Scenarios</h3>
            <p>The following scenarios demonstrate how small, actionable data-driven adjustments translate into immediate bottom-line improvements for individual dealerships.</p>

            <div class="scenario-box">
                <h4>Scenario 1: The "Baseload Burn" (1 kW Reduction)</h4>
                <p><strong>The Goal:</strong> Identify and eliminate 1 kW of "always-on" waste (e.g., showroom lighting or a high-wall HVAC left on overnight).</p>
                <div class="scenario-grid">
                    <div class="scenario-stat"><span class="lbl">Annual Units Saved</span><span class="val">8,760 kWh</span></div>
                    <div class="scenario-stat"><span class="lbl">Annual Cash Saving</span><span class="val" style="color:var(--color-success)">R36,115.73</span></div>
                    <div class="scenario-stat"><span class="lbl">Net Monthly Saving (incl. Fee)</span><span class="val">R2,759.64</span></div>
                    <div class="scenario-stat"><span class="lbl">Payback Period</span><span class="val" style="color:var(--color-primary)">≈ 2.1 Months</span></div>
                </div>
                <div style="margin-top: 16px; font-size: 13px; color: var(--color-muted); background: rgba(255,255,255,0.6); padding: 12px; border-radius: 6px;">
                    <strong>The Intelligence Factor:</strong> A 1 kW leak is completely invisible on a standard bulk municipal bill. Identifying this single "leak" covers the entire annual cost of the platform within the first quarter.
                </div>
            </div>

            <div class="scenario-box" style="border-color: #8b5cf6;">
                <h4 style="color: #8b5cf6;">Scenario 2: Critical Load Signaling (15% Efficiency Gain)</h4>
                <p><strong>The Goal:</strong> Using real-time alerts to manage "Maximum Demand" and optimized load profiles across a medium-sized dealership (averaging 25,000 kWh/month).</p>
                <div class="scenario-grid">
                    <div class="scenario-stat"><span class="lbl">Annual Energy Saving</span><span class="val">45,000 kWh</span></div>
                    <div class="scenario-stat"><span class="lbl">Annual Cash Saving</span><span class="val" style="color:var(--color-success)">R185,526.00</span></div>
                    <div class="scenario-stat"><span class="lbl">Net Monthly Saving (incl. Fee)</span><span class="val">R15,210.50</span></div>
                    <div class="scenario-stat"><span class="lbl">Payback Period</span><span class="val" style="color:#8b5cf6;">< 1 Month (approx 12 days)</span></div>
                </div>
            </div>

            <div class="scenario-box" style="border-color: var(--color-warning);">
                <h4 style="color: #d97706;">Scenario 3: Maximum Demand Clipping (Peak Shaving)</h4>
                <p><strong>The Goal:</strong> Using critical load signals to prevent non-essential equipment (e.g., valet pumps or geysers) from running concurrently during peak demand spikes.</p>
                <div style="margin-top: 12px;">
                    <p style="font-size: 14px;"><strong>The Problem:</strong> In Joburg and other metros, network capacity charges rose by over 18% this year. <br>
                    <strong>The ROI:</strong> Clipping just <strong>10 kVA</strong> from your notified demand can yield over <strong>R1,500 in monthly fixed-cost savings</strong> alone, irrespective of how many basic units (kWh) you use.</p>
                </div>
            </div>

            <div class="ui-mockup-wrapper" style="margin-top: 48px; padding: 32px;">
                <h3 style="margin-bottom: 8px;">Municipal Savings Matrix: 24/7 Baseload Reduction</h3>
                <p style="font-size: 14px; color: var(--color-muted); margin-bottom: 24px;">
                    The matrix below shows the annual cash impact (ZAR) of reducing your always-on baseload. <br>
                    <strong>Interactivity:</strong> Hover over any cell to see the specific formula and the municipal unit rate used for that calculation.
                </p>
                
                <div class="matrix-grid">
"""
# Build the matrix HTML programmatically
reductions = [1, 2, 3, 5, 10, 15, 20, 30]
rate = 4.1228
for kw in reductions:
    kwh = kw * 8760
    zar = kwh * rate
    # Format exactly.
    new_roi_section += f"""
                    <div class="matrix-cell">
                        <div class="kw-lbl">▼ {kw} kW</div>
                        <div class="val-lbl">R{zar:,.0f}</div>
                        <div class="matrix-tooltip">{kw} kW × 8,760 hr × R4.12/kWh</div>
                    </div>
"""

new_roi_section += """
                </div>
            </div>

            <div class="content-card" style="margin-top: 48px;">
                <h3 style="margin-bottom: 16px;">Why "Wait and See" is a R200,000 Mistake</h3>
                <p>The "Cost of Inaction" is currently at its highest point in South African history. Following the 2026 NERSA redetermination, electricity prices are projected to rise by a compound <strong>18.36% over the next 24 months</strong> (8.76% in 2026/27 and 8.83% in 2027/28).</p>
                
                <p style="margin-top: 16px; margin-bottom: 8px;"><strong>Energy Intelligence provides three critical advantages for 2026:</strong></p>
                <ol class="custom-bullet">
                    <li style="margin-bottom: 12px;"><strong>Benchmarking:</strong> Compare your Toyota, Mitsubishi, and Suzuki sites side-by-side. If one site has a baseload of 22 kW while another has 14 kW, you have found your first R280,000 in annual savings.</li>
                    <li style="margin-bottom: 12px;"><strong>Unbundling Protection:</strong> As municipalities move toward high fixed "Generation Capacity Charges," the only way to lower your bill is to decrease your notified demand (kVA). You cannot manage what you do not measure.</li>
                    <li style="margin-bottom: 12px;"><strong>The "Death Spiral" Hedge:</strong> As more businesses leave the grid, utilities are raising fixed costs for those who remain. Intelligence allows you to stay "lean" on the grid, minimizing your exposure to these systemic shifts.</li>
                </ol>
            </div>

            <div class="callout callout-accent" style="margin-top: 32px; background: rgba(16,185,129,0.05); border-left-color: var(--color-success);">
                <div class="callout-icon" style="color: var(--color-success);">
                    <svg class="icon icon-lg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <div class="callout-content">
                    <h3 style="color: var(--color-success);">Conclusion: Data as a Clean Fuel</h3>
                    <p>For CFAO Mobility, the implementation of a retail-focused measurement system is the first step in converting high-cost utility bills into high-value operational data. In an environment of 412 c/kWh, data isn't just information—it's the most profitable fuel you have.</p>
                </div>
            </div>
        </section>
"""

# We'll replace the existing section 8 (Investment & Return) with the new section
import re
# Regex to match the old Section 8 up to Section 9
pattern = re.compile(r'<!-- 8\. INVESTMENT & ROI -->.*?<!-- 9\. ABOUT AUGOS / CLOSING -->', re.DOTALL)
if pattern.search(html):
    html = pattern.sub(new_roi_section + '\n\n        <!-- 9. ABOUT AUGOS / CLOSING -->', html)
    print("Replaced section 8 successfully.")
else:
    print("Could not find section 8 to replace.")

with open(out_path, 'w') as f:
    f.write(html)

print("Generated V11!")
