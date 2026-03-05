import re

in_path = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V11.html'
out_path = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V12.html'

with open(in_path, 'r') as f:
    html = f.read()

# Split the document at HERO end and NEXT STEPS end
# Find end of hero
hero_end_marker = '        <!-- 1. EXECUTIVE SUMMARY & PHASE OVERVIEW -->'
header_part = html[:html.find(hero_end_marker)]
rest_part = html[html.find(hero_end_marker):]

footer_start_marker = '    </div>\n\n    <div class="footer">'
footer_part = rest_part[rest_part.find(footer_start_marker):]
sections_part = rest_part[:rest_part.find(footer_start_marker)]

# Split sections using regex. Each section roughly starts with <!-- X. TITLE --> and ends with </section>
# But wait, python split on <section> and </section> is safer.
# Let's cleanly extract each section block by identifying "<!-- N."
import copy

sections = []
# We know there are exactly 10 sections labelled like <!-- 1. ... --> to <!-- 10. ... -->
for i in range(1, 11):
    start_tag = f'<!-- {i}.'
    start_idx = sections_part.find(start_tag)
    if i < 10:
        end_idx = sections_part.find(f'<!-- {i+1}.')
        sections.append(sections_part[start_idx:end_idx])
    else:
        sections.append(sections_part[start_idx:])

# Reordering list:
# 1. Sec 8 (index 7) - The Financial Imperative
# 2. Sec 2 (index 1) - Specialist Retail Intelligence
# 3. Sec 3 (index 2) - The Augos Intelligence Platform
# 4. Sec 4 (index 3) - The Hardware Enabler
# 5. Sec 5 (index 4) - Active Fleet Management
# 6. Sec 1 (index 0) - Gain Strategic Control -> rename to Execution & Phase 1
# 7. Sec 7 (index 6) - Deployment Strategy
# 8. Sec 6 (index 5) - Competitive Overview
# 9. Sec 9 (index 8) - About Augos
# 10. Sec 10 (index -1) - Next Steps

order = [7, 1, 2, 3, 4, 0, 6, 5, 8, 9]

new_sections = []
for idx, o in enumerate(order):
    sec = sections[o]
    
    # Update section num inside the section
    # <div class="section-num">XX</div>
    old_num_str = f'0{o+1}' if o < 9 else f'{o+1}'
    new_num_str = f'0{idx+1}' if idx < 9 else f'{idx+1}'
    
    sec = re.sub(r'<div class="section-num">\d{2}</div>', f'<div class="section-num">{new_num_str}</div>', sec)
    
    # Also update the comment header to have the correct number (optional, but clean)
    sec = re.sub(r'<!-- \d+\.', f'<!-- {idx+1}.', sec, count=1)
    
    new_sections.append(sec)

# Fix title for Gain Strategic Control (now section 6)
# It used to be "Gain Strategic Control". Let's change it to "Phase 1: Proof of Value & Execution"
new_sections[5] = new_sections[5].replace('Gain Strategic Control', 'Execution & Phase 1 Scope')

# Connect back
final_body = "".join(new_sections)
final_html = header_part + final_body + footer_part

with open(out_path, 'w') as f:
    f.write(final_html)

print("Generated V12!")
