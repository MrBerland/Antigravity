import os
from google.cloud import bigquery

client = bigquery.Client(project="augos-core-data")
query = "SELECT category, question, answer FROM `augos-core-data.augos_warehouse.faqs`"
results = client.query(query).result()

with open("faqs_dump.txt", "w") as f:
    for row in results:
        f.write(f"Category: {row.category}\n")
        f.write(f"Q: {row.question}\n")
        f.write(f"A: {row.answer}\n")
        f.write("-" * 40 + "\n")
print("Done writing to faqs_dump.txt")
