import os
import sys

from google.cloud import bigquery

def main():
    client = bigquery.Client(project="augos-core-data")
    
    with open("kb_analysis.txt", "w") as f:
        f.write("--- KNOWLEDGE BASE OVERVIEW ---\n")
        
        # 1. Categories
        f.write("\n=== CATEGORIES ===\n")
        query = "SELECT category, COUNT(*) as cnt FROM `augos-core-data.augos_warehouse.knowledge_base` GROUP BY category ORDER BY cnt DESC"
        for row in client.query(query).result():
            f.write(f"{row[0]}: {row[1]}\n")

        # 2. Industries
        f.write("\n=== INDUSTRIES ===\n")
        query = "SELECT industry, COUNT(*) as cnt FROM `augos-core-data.augos_warehouse.knowledge_base` GROUP BY industry ORDER BY cnt DESC"
        for row in client.query(query).result():
            f.write(f"{row[0]}: {row[1]}\n")

        # 3. Features & Modules
        f.write("\n=== ALL TITLES AND SUMMARIES ===\n")
        query = "SELECT title, summary, category, industry FROM `augos-core-data.augos_warehouse.knowledge_base` ORDER BY category, title"
        for row in client.query(query).result():
            f.write(f"\n[{row.category} / {row.industry}] {row.title}\n")
            f.write(f"-> {row.summary}\n")
            
        # 4. FAQs
        f.write("\n=== FAQS OVERVIEW ===\n")
        try:
            query = "SELECT category, question, answer FROM `augos-core-data.augos_warehouse.faqs`"
            for row in client.query(query).result():
                f.write(f"\nQ: {row.question} ({row.category})\n")
                f.write(f"A: {row.answer[:150]}...\n")
        except Exception:
            f.write("No FAQs found.\n")

if __name__ == "__main__":
    main()
