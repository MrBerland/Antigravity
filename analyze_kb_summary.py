from google.cloud import bigquery
import json

client = bigquery.Client(project="augos-core-data")

def print_categories(table_id, group_col):
    print(f"\n--- {group_col.upper()} in {table_id} ---")
    try:
        query = f"SELECT {group_col}, COUNT(*) as cnt FROM `{table_id}` GROUP BY {group_col} ORDER BY cnt DESC LIMIT 15"
        results = client.query(query).result()
        for row in results:
            print(f"  {row[0]}: {row[1]}")
    except Exception as e:
        print(f"Error counting categories: {e}")

print_categories("augos-core-data.augos_warehouse.knowledge_base", "category")
print_categories("augos-core-data.augos_warehouse.knowledge_base", "industry")
print_categories("augos-core-data.augos_warehouse.knowledge_base", "content_type")

print_categories("augos-core-data.augos_warehouse.faqs", "category")

# Get high level summary of some interesting articles
print("\n--- SOME INTERESTING TOPICS (Knowledge Base) ---")
q = "SELECT title, summary FROM `augos-core-data.augos_warehouse.knowledge_base` WHERE category != 'Unknown' LIMIT 10"
res = client.query(q).result()
for r in res:
    print(f"* {r.title}\n  - {r.summary[:150]}")
