from google.cloud import bigquery
import json

client = bigquery.Client(project="augos-core-data")

def print_table_sample(table_id):
    print(f"\n--- {table_id} ---")
    try:
        table = client.get_table(table_id)
        print("SCHEMA:")
        for field in table.schema:
            print(f"  {field.name} ({field.field_type})")
            
        print("\nSAMPLE DATA (3 ROWS):")
        query = f"SELECT * FROM `{table_id}` LIMIT 3"
        results = client.query(query).result()
        for row in results:
            d = dict(row)
            # Truncate long strings for display
            for k, v in d.items():
                if isinstance(v, str) and len(v) > 200:
                    d[k] = v[:200] + "..."
            print(f"  {d}")
    except Exception as e:
        print(f"Error accessing {table_id}: {e}")

# Also group counts
def print_categories(table_id, group_col):
    print(f"\n--- Categories in {table_id} ---")
    try:
        query = f"SELECT {group_col}, COUNT(*) as cnt FROM `{table_id}` GROUP BY {group_col} ORDER BY cnt DESC"
        results = client.query(query).result()
        for row in results:
            print(f"  {row[0]}: {row[1]}")
    except Exception as e:
        print(f"Error counting categories: {e}")

print_table_sample("augos-core-data.augos_warehouse.knowledge_base")
print_categories("augos-core-data.augos_warehouse.knowledge_base", "category")

print_table_sample("augos-core-data.augos_warehouse.faqs")
print_categories("augos-core-data.augos_warehouse.faqs", "category")

print_table_sample("augos-core-data.hive_mind_core.dim_governance_rules")

