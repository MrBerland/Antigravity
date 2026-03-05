import os
import re

cfao_path = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V8.html'
out_path = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V9.html'

with open(cfao_path, 'r') as f:
    html = f.read()

css_to_inject = """
        /* EXTRA CSS FOR CFAO V9 */
        .three-col {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            margin-bottom: 24px
        }
        @media(max-width:1100px) {
            .three-col { grid-template-columns: 1fr }
        }
        .score-ring {
            width: 80px; height: 80px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: 700; position: relative; flex-shrink: 0;
            background: #e2e8f0;
        }
        .score-ring::before {
            content: ''; position: absolute; inset: 4px; border-radius: 50%; background: var(--color-background);
        }
        .score-ring span { position: relative; z-index: 1; color: var(--color-foreground); }
        .score-ring.green { background: conic-gradient(var(--color-success) calc(var(--pct) * 3.6deg), #e2e8f0 0deg); }
        .score-ring.amber { background: conic-gradient(var(--color-warning) calc(var(--pct) * 3.6deg), #e2e8f0 0deg); }
        .score-ring.red { background: conic-gradient(var(--color-danger) calc(var(--pct) * 3.6deg), #e2e8f0 0deg); }

        .summary-card-inner {
            display: flex; align-items: center; gap: 16px; padding: 20px;
        }
        .summary-card-inner .details { flex: 1; }
        .summary-card-inner .details h3 { font-size: 14px; font-weight: 600; margin-bottom: 8px; color: var(--color-foreground); }
        .summary-card-inner .detail-row {
            display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; border-bottom: 1px solid var(--color-border);
        }
        .summary-card-inner .detail-row:last-child { border-bottom: none; }
        .summary-card-inner .detail-row .label { color: var(--color-muted); }

        .kpi-row {
            display: grid; grid-template-columns: repeat(2, 1fr);
            padding: 12px 16px 0; gap: 16px;
        }
        .kpi-row .kpi { padding: 10px 12px; }
        .kpi-label { font-size: 12px; color: var(--color-muted); font-weight: 500; margin-bottom: 4px; }
        .kpi-value { font-size: 22px; font-weight: 700; line-height: 1.2; color: var(--color-foreground); }
        .kpi-sub { font-size: 12px; color: var(--color-muted); margin-top: 4px; }
        .kpi-sub .down { color: var(--color-success); font-weight: 600; }
        .kpi-sub .up { color: var(--color-danger); font-weight: 600; }

        .scatter-wrap { position: relative; width: 100%; height: 440px; padding: 30px 40px 44px 56px; }
        .scatter-area { position: relative; width: 100%; height: 100%; border-left: 2px solid #e2e8f0; border-bottom: 2px solid #e2e8f0; overflow: visible; font-family: 'Inter', sans-serif; }
        .scatter-qline-h { position: absolute; left: 0; right: 0; border-top: 1.5px dashed rgba(148, 163, 184, .35); z-index: 1; }
        .scatter-qline-v { position: absolute; top: 0; bottom: 0; border-left: 1.5px dashed rgba(148, 163, 184, .35); z-index: 1; }
        .quad-zone { position: absolute; display: flex; flex-direction: column; padding: 8px 10px; pointer-events: none; }
        .quad-name { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .7px; margin-bottom: 1px; }
        .quad-desc { font-size: 9px; font-weight: 400; line-height: 1.3; opacity: .6; }
        .bubble {
            position: absolute; border-radius: 50%; transform: translate(-50%, 50%);
            cursor: pointer; transition: transform .2s, box-shadow .2s;
            display: flex; align-items: center; justify-content: center;
            font-size: 0; font-weight: 600; color: #fff;
            border: 2px solid rgba(255, 255, 255, .8);
            box-shadow: 0 1px 4px rgba(0, 0, 0, .15);
        }
        .bubble:hover { transform: translate(-50%, 50%) scale(1.2); box-shadow: 0 4px 16px rgba(0, 0, 0, .3); z-index: 10; }
        .bubble-tip {
            display: none; position: absolute; bottom: calc(100% + 10px); left: 50%; transform: translateX(-50%);
            background: #0f172a; color: #fff; padding: 8px 12px; border-radius: 8px;
            font-size: 11px; white-space: nowrap; z-index: 20; pointer-events: none; line-height: 1.5;
        }
        .bubble-tip::after {
            content: ''; position: absolute; top: 100%; left: 50%; transform: translateX(-50%);
            border: 5px solid transparent; border-top-color: #0f172a;
        }
        .bubble:hover .bubble-tip { display: block; }
        .scatter-ax-x { position: absolute; bottom: -34px; left: 50%; transform: translateX(-50%); font-size: 11px; font-weight: 600; color: var(--color-muted); }
        .scatter-ax-y { position: absolute; left: -48px; top: 50%; transform: translateY(-50%) rotate(-90deg); font-size: 11px; font-weight: 600; color: var(--color-muted); white-space: nowrap; }
        .scatter-tick { position: absolute; font-size: 9px; color: var(--color-muted); }
        .scatter-tick.x-tick { bottom: -14px; transform: translateX(-50%); }
        .scatter-tick.y-tick { left: -26px; transform: translateY(50%); }

        .chart-legend { display: flex; gap: 16px; padding: 0 20px 16px; font-size: 12px; color: var(--color-muted); margin-top:20px; }
        .chart-legend i { width: 12px; height: 12px; border-radius: 2px; display: inline-block; vertical-align: middle; margin-right: 4px; }
"""

html = html.replace('</style>', css_to_inject + '\n    </style>')

cards_html = """
            <h3 style="margin-top: 64px; margin-bottom: 24px;">Executive Performance Dashboards</h3>
            <p>Moving away from static PDFs, the platform provides beautiful, real-time macro-level visibility natively aligning with CFAO’s strategic objectives.</p>
            
            <div class="three-col">
                <!-- Energy Performance -->
                <div class="ui-mockup-wrapper" style="margin: 0; display:flex; flex-direction:column;">
                    <div class="ui-mockup-header" style="border-bottom:1px solid var(--color-border); padding:12px 16px">
                        <div class="ui-mockup-title" style="color:#f59e0b">⚡ Energy Performance</div>
                    </div>
                    <div class="kpi-row">
                        <div class="kpi">
                            <div class="kpi-label">Consumption (MTD)</div>
                            <div class="kpi-value">441 <small style="font-size:11px;font-weight:400">MWh</small></div>
                            <div class="kpi-sub"><span class="down">▼ 8.2%</span> vs prior</div>
                        </div>
                        <div class="kpi">
                            <div class="kpi-label">Reduction vs V₄</div>
                            <div class="kpi-value" style="color:var(--color-success)">−12.4%</div>
                            <div class="kpi-sub">Since baseline</div>
                        </div>
                    </div>
                    <div class="summary-card-inner" style="border-top:1px solid #f1f5f9; margin-top:auto">
                        <div class="score-ring green" style="--pct:82"><span>82</span></div>
                        <div class="details">
                            <h3>Efficiency Score</h3>
                            <div class="detail-row"><span class="label">Avg kWh/m²</span><span class="value">8.6</span></div>
                            <div class="detail-row"><span class="label">After-hours ratio</span><span class="value">36% <span style="color:var(--color-success);font-size:11px">▼ 42%</span></span></div>
                            <div class="detail-row"><span class="label">Least efficient</span><span class="value" style="color:var(--color-danger)">CFAO Ford CT</span></div>
                        </div>
                    </div>
                </div>

                <!-- Carbon & Compliance -->
                <div class="ui-mockup-wrapper" style="margin: 0; display:flex; flex-direction:column;">
                    <div class="ui-mockup-header" style="border-bottom:1px solid var(--color-border); padding:12px 16px">
                        <div class="ui-mockup-title" style="color:#10b981">🌱 Carbon & Compliance</div>
                    </div>
                    <div class="kpi-row">
                        <div class="kpi">
                            <div class="kpi-label">Scope 2 (MTD)</div>
                            <div class="kpi-value">468 <small style="font-size:11px;font-weight:400">tCO₂e</small></div>
                            <div class="kpi-sub"><span class="down">▼ 5.1%</span> vs prior</div>
                        </div>
                        <div class="kpi">
                            <div class="kpi-label">Carbon Tax Risk</div>
                            <div class="kpi-value">R210K</div>
                            <div class="kpi-sub">@ R450/tCO₂e</div>
                        </div>
                    </div>
                    <div class="summary-card-inner" style="border-top:1px solid #f1f5f9; margin-top:auto">
                        <div class="score-ring green" style="--pct:78"><span>78</span></div>
                        <div class="details">
                            <h3>ESG Trajectory</h3>
                            <div class="detail-row"><span class="label">Grid Factor</span><span class="value">1.06 kgCO₂/kWh</span></div>
                            <div class="detail-row"><span class="label">Reduction target</span><span class="value">10% by Dec 26</span></div>
                            <div class="detail-row"><span class="label">Trajectory</span><span class="value" style="color:var(--color-success)">On track</span></div>
                        </div>
                    </div>
                </div>

                <!-- Operational Health -->
                <div class="ui-mockup-wrapper" style="margin: 0; display:flex; flex-direction:column;">
                    <div class="ui-mockup-header" style="border-bottom:1px solid var(--color-border); padding:12px 16px">
                        <div class="ui-mockup-title" style="color:#3b82f6">⚡ Operational Health</div>
                    </div>
                    <div class="kpi-row">
                        <div class="kpi">
                            <div class="kpi-label">Telemetry Online</div>
                            <div class="kpi-value">92<small style="font-size:13px;font-weight:400"> / 100</small></div>
                            <div class="kpi-sub">92% connectivity</div>
                        </div>
                        <div class="kpi">
                            <div class="kpi-label">Avg Alert TTR</div>
                            <div class="kpi-value">14 <small style="font-size:11px;font-weight:400">min</small></div>
                            <div class="kpi-sub">87% < 30 min</div>
                        </div>
                    </div>
                    <div class="summary-card-inner" style="border-top:1px solid #f1f5f9; margin-top:auto">
                        <div class="score-ring amber" style="--pct:71"><span>71</span></div>
                        <div class="details">
                            <h3>Portfolio Health Score</h3>
                            <div class="detail-row"><span class="label">Sites on target</span><span class="value" style="color:var(--color-success)">65 / 100 </span></div>
                            <div class="detail-row"><span class="label">Attention required</span><span class="value" style="color:var(--color-warning)">25 / 100</span></div>
                            <div class="detail-row"><span class="label">Critical anomalies</span><span class="value" style="color:var(--color-danger)">10 (Inc. VW Midrand)</span></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="ui-mockup-wrapper" style="margin-top: 40px; margin-bottom: 64px;">
                <div class="ui-mockup-header">
                    <div>
                        <div class="ui-mockup-title" style="color: var(--color-foreground);">Site Performance Map</div>
                        <div style="font-size:12px; color:var(--color-muted); margin-top:4px; font-family:'Inter',sans-serif;">Trading vs Overnight compliance · Bubble size = Total kWh</div>
                    </div>
                </div>
                <div class="scatter-wrap">
                    <div class="scatter-area" id="scatterPlot"></div>
                </div>
                <div class="chart-legend">
                    <span><i style="background:var(--color-success);border-radius:50%"></i> On target</span>
                    <span><i style="background:var(--color-warning);border-radius:50%"></i> Watch</span>
                    <span><i style="background:var(--color-danger);border-radius:50%"></i> Action needed</span>
                </div>
                <div class="insight-card">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10" />
                        <line x1="12" y1="16" x2="12" y2="12" />
                        <line x1="12" y1="8" x2="12.01" y2="8" />
                    </svg>
                    <div><strong>AI Insight:</strong> CFAO VW Midrand (bottom-left, largest bubble) consumes highest absolute load while displaying poor compliance on both trading and after-hours tracking — this represents the highest singular ROI opportunity for immediate intervention across the portfolio. CFAO Ford Upington (top-right) serves as the network benchmark.</div>
                </div>
            </div>
"""

index = html.find('<h3>Hyper-Accurate NERSA Tariff Database</h3>')
if index != -1:
    insert_idx = html.rfind('<div class="content-card">', 0, index)
    if insert_idx != -1:
        html = html[:insert_idx] + cards_html + html[insert_idx:]
        print("Successfully found insertion point.")
    else:
        print("Could not find <div class='content-card'> before H3")
else:
    print("Could not find H3")


script_to_inject = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const scatterSites = [
                { name: 'CFAO Ford Upington', trad: 95, night: 92, kwh: 180 },
                { name: 'Toyota Aliwal North', trad: 92, night: 88, kwh: 110 },
                { name: 'VW Graaff-Reinet', trad: 90, night: 85, kwh: 120 },
                { name: 'Hino Bethlehem', trad: 90, night: 82, kwh: 130 },
                { name: 'Toyota Newcastle', trad: 88, night: 72, kwh: 165 },
                { name: 'Ford Kimberley', trad: 86, night: 78, kwh: 145 },
                { name: 'VW Polokwane', trad: 85, night: 55, kwh: 175 },
                { name: 'CFAO Welkom', trad: 83, night: 70, kwh: 160 },
                { name: 'Toyota Boksburg', trad: 82, night: 45, kwh: 245 },
                { name: 'VW Springs', trad: 80, night: 65, kwh: 155 },
                { name: 'Ford Bloemfontein', trad: 78, night: 40, kwh: 220 },
                { name: 'Hino Middelburg', trad: 77, night: 60, kwh: 140 },
                { name: 'Toyota Witbank', trad: 75, night: 38, kwh: 195 },
                { name: 'CFAO VW Midrand', trad: 60, night: 25, kwh: 310 },
            ];
            const area = document.getElementById('scatterPlot');
            if (!area) return;
            const minAxis = 20, maxAxis = 100, threshold = 80;
            const range = maxAxis - minAxis;
            const maxKwh = Math.max(...scatterSites.map(s => s.kwh));
            const minBubble = 14, maxBubble = 44;

            const qPct = ((threshold - minAxis) / range) * 100;
            area.innerHTML = `
                <div class="quad-zone" style="left:${qPct}%;right:0;top:0;bottom:${100 - qPct}%;background:rgba(16,185,129,.06);justify-content:flex-start;align-items:flex-end">
                    <div class="quad-name" style="color:var(--color-success)">Best Practice</div>
                    <div class="quad-desc" style="color:var(--color-success)">Compliant on both dimensions</div>
                </div>
                <div class="quad-zone" style="left:0;right:${100 - qPct}%;top:0;bottom:${100 - qPct}%;background:rgba(36,99,235,.05);justify-content:flex-start;align-items:flex-start">
                    <div class="quad-name" style="color:var(--color-primary)">Trading Risk</div>
                    <div class="quad-desc" style="color:var(--color-primary)">Good overnight, weak trading hours</div>
                </div>
                <div class="quad-zone" style="left:${qPct}%;right:0;top:${qPct}%;bottom:0;background:rgba(245,158,11,.05);justify-content:flex-end;align-items:flex-end">
                    <div class="quad-name" style="color:var(--color-warning)">Overnight Risk</div>
                    <div class="quad-desc" style="color:var(--color-warning)">Good trading, weak after-hours</div>
                </div>
                <div class="quad-zone" style="left:0;right:${100 - qPct}%;top:${qPct}%;bottom:0;background:rgba(239,68,68,.05);justify-content:flex-end;align-items:flex-start">
                    <div class="quad-name" style="color:var(--color-danger)">Priority Intervention</div>
                    <div class="quad-desc" style="color:var(--color-danger)">Below target on both dimensions</div>
                </div>
                <div class="scatter-qline-h" style="bottom:${qPct}%"></div>
                <div class="scatter-qline-v" style="left:${qPct}%"></div>
                <div class="scatter-ax-x">Trading Load Compliance →</div>
                <div class="scatter-ax-y">Overnight Load Compliance →</div>
            `;

            [40, 60, 80, 100].forEach(v => {
                const pct = ((v - minAxis) / range) * 100;
                area.innerHTML += `<div class="scatter-tick x-tick" style="left:${pct}%">${v}%</div>`;
                area.innerHTML += `<div class="scatter-tick y-tick" style="bottom:${pct}%">${v}%</div>`;
            });

            scatterSites.forEach(s => {
                const x = ((s.trad - minAxis) / range) * 100;
                const y = ((s.night - minAxis) / range) * 100;
                const size = minBubble + ((s.kwh / maxKwh) * (maxBubble - minBubble));
                const both = s.trad >= threshold && s.night >= threshold;
                const either = s.trad >= threshold || s.night >= threshold;
                const color = both ? 'var(--color-success)' : either ? 'var(--color-warning)' : 'var(--color-danger)';
                area.innerHTML += `<div class="bubble" style="left:${x}%;bottom:${y}%;width:${size}px;height:${size}px;background:${color}">
                    <div class="bubble-tip" style="background:var(--color-foreground);">
                        <strong>${s.name}</strong><br>
                        Trading: ${s.trad}% · Overnight: ${s.night}%<br>
                        Daily load: ${s.kwh} kWh
                    </div>
                </div>`;
            });
        });
    </script>
</body>
"""

html = html.replace('</body>', script_to_inject)

with open(out_path, 'w') as f:
    f.write(html)

print("Generated V9!")
