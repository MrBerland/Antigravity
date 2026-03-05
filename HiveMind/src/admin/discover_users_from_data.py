from google.cloud import bigquery
import os
import json
import re

PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE
CONFIG_FILE = os.path.abspath('HiveMind/config/users_list.json')

# 1. Hardcoded Manual List (from User Request)
manual_users = [
    'tim@augos.io',
    'maretha@augos.io',
    'chris@augos.io',
    'oliver@augos.io',
    'support@augos.io',
    'tim+canned.response@augos.io',
    'mary-anne@augos.io',
    'angela@augos.io',
    'james@augos.io',
    'lizl@augos.io',
    'beate@augos.io',
    'abrie@augos.io',
    'eduan@augos.io',
    'sean@augos.io'
]

def discover_users():
    client = bigquery.Client(project=PROJECT_ID)
    
    # Query to find any email address ending in @augos.io
    # We look at Senders (high confidence)
    # We could look at Recipients too, but that might catch aliases or groups. 
    # For "Ingestion", we need real accounts. Senders is a good proxy for active accounts.
    query = """
    SELECT DISTINCT sender
    FROM `augos-core-data.hive_mind_core.staging_raw_emails`
    WHERE sender LIKE '%@augos.io%'
    """
    
    print("🔎 Mining BigQuery for @augos.io addresses...")
    discovered = set()
    
    try:
        rows = client.query(query).result()
        email_pattern = r'[\w\.-]+@augos\.io'
        
        for row in rows:
            # Extract email from "Name <email>" string
            match = re.search(email_pattern, row.sender)
            if match:
                email = match.group(0).lower()
                # Exclude system/no-reply if possible, but for now allow them (might be shared mailboxes)
                discovered.add(email)
                
    except Exception as e:
        print(f"⚠️ Query failed: {e}")

    # Merge Lists
    final_list = set(manual_users) | discovered
    
    # Sort for stability
    sorted_list = sorted(list(final_list))
    
    print(f"✅ User Discovery Complete.")
    print(f"   - Manual: {len(manual_users)}")
    print(f"   - Discovered: {len(discovered)}")
    print(f"   - Total Unique: {len(sorted_list)}")
    
    # Save to Config
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(sorted_list, f, indent=2)
    print(f"💾 Saved to {CONFIG_FILE}")
    
    return sorted_list

if __name__ == "__main__":
    users = discover_users()
    for u in users:
        print(f" - {u}")
