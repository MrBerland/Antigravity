from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project="augos-core-data")

print("--- knowledge_base SCHEMA ---")
try:
    kb_table = client.get_table("augos-core-data.augos_warehouse.knowledge_base")
    for schema_field in kb_table.schema:
        print(f"{schema_field.name}: {schema_field.field_type}")
except Exception as e:
    print(f"Error fetching schema for knowledge_base: {e}")

print("\n--- SAMPLE knowledge_base DATA ---")
try:
    query_job = client.query("SELECT * FROM `augos-core-data.augos_warehouse.knowledge_base` LIMIT 5")
    results = query_job.result()
    for row in results:
        print(dict(row))
except Exception as e:
    print(e)
    
print("\n--- FAQS SCHEMA ---")
try:
    faq_table = client.get_table("augos-core-data.augos_warehouse.faqs")
    for schema_field in faq_table.schema:
        print(f"{schema_field.name}: {schema_field.field_type}")
except Exception as e:
    pass

