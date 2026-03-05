import fitz
doc = fitz.open('/Users/timstevens/Website v2/UI images/Strategic Energy Intelligence & Solar Investment Proposal.pdf')
text = ""
for page in doc:
    text += page.get_text()
with open('extracted.txt', 'w') as f:
    f.write(text)
print("Extracted PDF to extracted.txt")
