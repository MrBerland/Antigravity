from google.cloud import bigquery
import os

try:
    client = bigquery.Client(project="augos-core-data")
    datasets = list(client.list_datasets())
    print("Datasets in project:")
    for dataset in datasets:
        print(dataset.dataset_id)
        
    print("\nTables in knowledge:")
    try:
        tables = client.list_tables("augos-core-data.knowledge")
        for table in tables:
            print(f" - {table.table_id}")
    except Exception as e:
        print(f"Error reading knowledge: {e}")
        
    print("\nTables in documents:")
    try:
        tables = client.list_tables("augos-core-data.documents")
        for table in tables:
            print(f" - {table.table_id}")
    except Exception as e:
        print(f"Error reading documents: {e}")
        
except Exception as e:
    print(f"General error: {e}")
