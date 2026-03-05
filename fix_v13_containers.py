"""Map V12's section structure — find every <section>...</section> boundary and verify div balance"""
import re

path = '/Users/timstevens/Website v2/UI images/CFAO_Mobility_Proposal_V12.html'

with open(path) as f:
    lines = f.readlines()

sections = []
in_section = False
sec_start = None
sec_depth = 0

for i, line in enumerate(lines):
    ln = i + 1
    s = line.strip()
    
    if s == '<section>':
        in_section = True
        sec_start = ln
        sec_depth = 0
        
    if in_section:
        sec_depth += line.count('<div') - line.count('</div')
    
    if s == '</section>' and in_section:
        in_section = False
        # Find the heading
        heading = ''
        for j in range(sec_start - 1, min(sec_start + 10, len(lines))):
            if 'section-title' in lines[j]:
                import re
                m = re.search(r'>([^<]+)<', lines[j])
                if m:
                    heading = m.group(1).strip()
                    break
            if 'section-num' in lines[j]:
                m2 = re.search(r'>(\d+)<', lines[j])
                if m2:
                    heading = f"[{m2.group(1)}] "
        
        sections.append({
            'start': sec_start,
            'end': ln,
            'heading': heading,
            'div_balance': sec_depth,
            'lines': ln - sec_start + 1
        })

print(f"Found {len(sections)} sections in V12:\n")
for s in sections:
    bal = "✅" if s['div_balance'] == 0 else f"❌ ({s['div_balance']:+d})"
    print(f"  Lines {s['start']:4d}-{s['end']:4d} ({s['lines']:3d} lines) | div-bal: {bal} | {s['heading']}")

# Also find header and footer boundaries
print(f"\nHeader: lines 1-{sections[0]['start']-1}")
print(f"Footer: lines {sections[-1]['end']+1}-{len(lines)}")

# Check what's immediately before first section
print(f"\nLines just before first section:")
for i in range(sections[0]['start'] - 5, sections[0]['start']):
    print(f"  {i+1}: {lines[i].rstrip()[:80]}")

# Check what's immediately after last section
print(f"\nLines just after last section:")
for i in range(sections[-1]['end'], min(sections[-1]['end'] + 5, len(lines))):
    print(f"  {i+1}: {lines[i].rstrip()[:80]}")
