import os

in_path = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V9.html'
out_path = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V10.html'

with open(in_path, 'r') as f:
    html = f.read()

css_to_inject = """
        /* Fleet & Grid */
        .fleet-bar { display: flex; height: 6px; border-radius: 3px; overflow: hidden; background: #e2e8f0; }
        .fleet-bar .online { background: var(--color-success); }
        .fleet-bar .offline { background: var(--color-danger); }
        .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; vertical-align: middle; }
        .dot-green { background: var(--color-success); }
        .dot-red { background: var(--color-danger); }
        
        .device-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; padding: 16px; background: #f8fafc; }
        .device-card { border: 1px solid var(--color-border); border-radius: 8px; padding: 14px; position: relative; background: #fff; }
        .device-card.online { border-left: 3px solid var(--color-success); }
        .device-card.offline { border-left: 3px solid var(--color-danger); }
        .device-name { font-weight: 600; font-size: 13px; margin-bottom: 4px; color: var(--color-foreground); }
        .device-meta { font-size: 11px; color: var(--color-muted); }
        .device-signal { position: absolute; top: 14px; right: 14px; display: flex; align-items: flex-end; gap: 2px; height: 14px; }
        .device-signal span { width: 3px; border-radius: 1px; }
        .device-signal .sig-on { background: var(--color-success); }
        .device-signal .sig-off { background: var(--color-danger); }
"""

html = html.replace('</style>', css_to_inject + '\n    </style>')

# Shift section numbers up
html = html.replace('<!-- 5. COMPETITIVE COMPARISON -->', '<!-- 6. COMPETITIVE COMPARISON -->')
html = html.replace('<div class="section-num">05</div>\n                <h2 class="section-title">Competitive Overview</h2>', '<div class="section-num">06</div>\n                <h2 class="section-title">Competitive Overview</h2>')

html = html.replace('<!-- 6. STRATEGIC DEPLOYMENT -->', '<!-- 7. STRATEGIC DEPLOYMENT -->')
html = html.replace('<div class="section-num">06</div>\n                <h2 class="section-title">Deployment Strategy</h2>', '<div class="section-num">07</div>\n                <h2 class="section-title">Deployment Strategy</h2>')

html = html.replace('<!-- 7. INVESTMENT & ROI -->', '<!-- 8. INVESTMENT & ROI -->')
html = html.replace('<div class="section-num">07</div>\n                <h2 class="section-title">Investment & Return</h2>', '<div class="section-num">08</div>\n                <h2 class="section-title">Investment & Return</h2>')

html = html.replace('<!-- 8. ABOUT AUGOS / CLOSING -->', '<!-- 9. ABOUT AUGOS / CLOSING -->')
html = html.replace('<div class="section-num">08</div>\n                <h2 class="section-title">About Augos</h2>', '<div class="section-num">09</div>\n                <h2 class="section-title">About Augos</h2>')

html = html.replace('<!-- 9. NEXT STEPS -->', '<!-- 10. NEXT STEPS -->')


fleet_section = """
        <!-- 5. ACTIVE FLEET & INTERVENTION MANAGEMENT -->
        <section>
            <div class="section-header">
                <div class="section-num">05</div>
                <h2 class="section-title">Active Fleet Management</h2>
            </div>
            
            <p>For large-scale, multi-site operations, the physical integrity of the telemetry fleet is mission-critical. South Africa's geography is enormous — ensuring reliable data continuity from a dealership in Mbombela to Cape Town, or from Upington to Richards Bay, presents a significant operational challenge that the Augos platform natively conquers.</p>
            
            <p>Rather than leaving you blind to offline sites, our platform actively monitors and reports the health, OTA (Over-The-Air) success rate, and data latency of every installed meter. When physical intervention is genuinely required, we keep costs exceptionally low: our proprietary mobile installation app allows any of your contracted, trusted local electricians to quickly swap or service devices, completely skipping the exorbitant travel costs of specialist deployment engineers.</p>

            <div class="ui-mockup-wrapper" style="margin-top: 40px;">
                <div class="ui-mockup-header" style="border-bottom:none">
                    <div class="ui-mockup-title" style="color:var(--color-foreground)">Fleet Status Overview</div>
                </div>
                <div style="padding:0 24px 24px;">
                    <div style="font-size:13px; color:var(--color-muted); margin-bottom: 24px;">Device health, connectivity, and installation tracking for the CFAO network.</div>
                    
                    <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:16px; margin-bottom:24px;">
                        <div style="border:1px solid var(--color-border); border-radius:8px; padding:16px; background:#fff; box-shadow:var(--shadow-sm)">
                            <div style="font-size:12px; color:var(--color-muted); font-weight:500; margin-bottom:8px">Devices Deployed</div>
                            <div style="font-size:24px; font-weight:700; margin-bottom:8px; color:var(--color-foreground)">100</div>
                            <div class="fleet-bar">
                                <div class="online" style="width:92%"></div>
                                <div class="offline" style="width:8%"></div>
                            </div>
                            <div style="font-size:12px; color:var(--color-muted); margin-top:8px; display:flex; gap:12px">
                                <span><span class="dot dot-green"></span> 92 online</span>
                                <span><span class="dot dot-red"></span> 8 offline</span>
                            </div>
                        </div>
                        <div style="border:1px solid var(--color-border); border-radius:8px; padding:16px; background:#fff; box-shadow:var(--shadow-sm)">
                            <div style="font-size:12px; color:var(--color-muted); font-weight:500; margin-bottom:8px">OTA Success Rate</div>
                            <div style="font-size:24px; font-weight:700; color:var(--color-success); margin-bottom:8px">100%</div>
                            <div style="font-size:12px; color:var(--color-muted);">All verified on first attempt</div>
                        </div>
                        <div style="border:1px solid var(--color-border); border-radius:8px; padding:16px; background:#fff; box-shadow:var(--shadow-sm)">
                            <div style="font-size:12px; color:var(--color-muted); font-weight:500; margin-bottom:8px">Avg Data Latency</div>
                            <div style="font-size:24px; font-weight:700; margin-bottom:8px; color:var(--color-foreground)">2.1 <span style="font-size:14px; font-weight:500; color:var(--color-muted)">min</span></div>
                            <div style="font-size:12px; color:var(--color-muted);">Target: < 5 min</div>
                        </div>
                    </div>

                    <div style="border:1px solid var(--color-border); border-radius:8px; background:#fff; overflow:hidden">
                        <div style="padding:16px; border-bottom:1px solid var(--color-border); display:flex; justify-content:space-between; align-items:center;">
                            <div style="font-weight:600; font-size:14px; color:var(--color-foreground)">Device Grid <span style="color:var(--color-muted);font-weight:400;margin-left:4px">(Live)</span></div>
                        </div>
                        <div class="device-grid">
                            <div class="device-card online">
                                <div class="device-signal"><span class="sig-on" style="height:6px"></span><span class="sig-on" style="height:9px"></span><span class="sig-on" style="height:12px"></span><span class="sig-on" style="height:14px"></span></div>
                                <div class="device-name">CFAO VW Midrand</div>
                                <div class="device-meta">Last data: 1 min ago</div>
                                <div class="device-meta" style="margin-top:4px">✅ OTA Verified</div>
                            </div>
                            <div class="device-card online">
                                <div class="device-signal"><span class="sig-on" style="height:6px"></span><span class="sig-on" style="height:9px"></span><span class="sig-on" style="height:12px"></span><span class="sig-on" style="height:14px"></span></div>
                                <div class="device-name">Toyota Boksburg</div>
                                <div class="device-meta">Last data: 2 min ago</div>
                                <div class="device-meta" style="margin-top:4px">✅ OTA Verified</div>
                            </div>
                            <div class="device-card offline">
                                <div class="device-signal"><span class="sig-off" style="height:6px"></span></div>
                                <div class="device-name">Ford Bloemfontein</div>
                                <div class="device-meta">Last seen: 4h ago</div>
                                <div class="device-meta" style="margin-top:4px; color:var(--color-danger)">⚠️ Connection lost</div>
                            </div>
                            <div class="device-card online">
                                <div class="device-signal"><span class="sig-on" style="height:6px"></span><span class="sig-on" style="height:9px"></span><span class="sig-on" style="height:12px"></span><span class="sig-on" style="height:14px"></span></div>
                                <div class="device-name">Hino Middelburg</div>
                                <div class="device-meta">Last data: 2 min ago</div>
                                <div class="device-meta" style="margin-top:4px">✅ OTA Verified</div>
                            </div>
                            <div class="device-card online">
                                <div class="device-signal"><span class="sig-on" style="height:6px"></span><span class="sig-on" style="height:9px"></span><span class="sig-on" style="height:12px"></span><span class="sig-on" style="height:14px"></span></div>
                                <div class="device-name">Ford Upington</div>
                                <div class="device-meta">Last data: 3 min ago</div>
                                <div class="device-meta" style="margin-top:4px">✅ OTA Verified</div>
                            </div>
                            <div class="device-card online">
                                <div class="device-signal"><span class="sig-on" style="height:6px"></span><span class="sig-on" style="height:9px"></span><span class="sig-on" style="height:12px"></span><span class="sig-on" style="height:14px"></span></div>
                                <div class="device-name">Toyota Aliwal N.</div>
                                <div class="device-meta">Last data: 1 min ago</div>
                                <div class="device-meta" style="margin-top:4px">✅ OTA Verified</div>
                            </div>
                            <div class="device-card online">
                                <div class="device-signal"><span class="sig-on" style="height:6px"></span><span class="sig-on" style="height:9px"></span><span class="sig-on" style="height:12px"></span><span class="sig-on" style="height:14px"></span></div>
                                <div class="device-name">VW Graaff-Reinet</div>
                                <div class="device-meta">Last data: 2 min ago</div>
                                <div class="device-meta" style="margin-top:4px">✅ OTA Verified</div>
                            </div>
                            <div class="device-card offline">
                                <div class="device-signal"><span class="sig-off" style="height:6px"></span></div>
                                <div class="device-name">Ford Kimberley</div>
                                <div class="device-meta">Last seen: 2h ago</div>
                                <div class="device-meta" style="margin-top:4px; color:var(--color-danger)">⚠️ Connection lost</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>\n
"""

insert_idx = html.find('<!-- 6. COMPETITIVE COMPARISON -->')
if insert_idx != -1:
    html = html[:insert_idx] + fleet_section + html[insert_idx:]
    print("Inserted new Fleet Management section successfully.")
else:
    print("Could not find insertion point.")

with open(out_path, 'w') as f:
    f.write(html)

print("Generated V10!")

