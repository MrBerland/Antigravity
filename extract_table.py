import pdfplumber

with pdfplumber.open('/Users/timstevens/Website v2/UI images/Strategic Energy Intelligence & Solar Investment Proposal.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for t_idx, table in enumerate(tables):
            print(f"Page {i+1}, Table {t_idx+1}:")
            for row in table:
                print(row)
            print("-" * 40)
