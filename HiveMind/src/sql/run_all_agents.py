"""
HiveMind Agent Runner
=====================
Runs all four AI analysis agents sequentially with retry logic
to handle BigQuery ML.GENERATE_TEXT rate limits.

Usage:
    python3 HiveMind/src/sql/run_all_agents.py
    
    # Or with custom batch size and max retries:
    python3 HiveMind/src/sql/run_all_agents.py --batch 25 --retries 5
"""

from google.cloud import bigquery
import os
import time
import argparse

# Configuration
PROJECT_ID = 'augos-core-data'
SERVICE_ACCOUNT_FILE = os.path.abspath('HiveMind/credentials/hive-mind-admin.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE


def run_agent(client, name, query, max_retries=3):
    """Run a single agent procedure with exponential backoff on rate limit errors."""
    for attempt in range(1, max_retries + 1):
        print(f"\n🔄 [{name}] Attempt {attempt}/{max_retries}...")
        try:
            job = client.query(query)
            job.result(timeout=600)
            print(f"✅ [{name}] Completed successfully!")
            return True
        except Exception as e:
            error_str = str(e)
            if "rate limits" in error_str.lower() or "too many concurrent" in error_str.lower():
                wait_time = 60 * attempt  # 60s, 120s, 180s...
                print(f"⏳ [{name}] Rate limited. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"❌ [{name}] Non-retryable error: {e}")
                return False
    
    print(f"❌ [{name}] Exhausted all {max_retries} retries.")
    return False


def main():
    parser = argparse.ArgumentParser(description="Run HiveMind AI agents")
    parser.add_argument("--batch", type=int, default=50, help="Batch size per agent (default: 50)")
    parser.add_argument("--retries", type=int, default=3, help="Max retries per agent (default: 3)")
    parser.add_argument("--cooldown", type=int, default=60, help="Seconds to wait between agents (default: 60)")
    args = parser.parse_args()

    client = bigquery.Client(project=PROJECT_ID)
    batch = args.batch

    agents = [
        ("Support Thread Scorer", f"CALL `hive_mind_core.analyze_support_threads`({batch})"),
        ("Question Extractor",    f"CALL `hive_mind_core.analyze_questions`({batch})"),
        ("Sales Lead Scorer",     f"CALL `hive_mind_core.analyze_sales_leads`({batch})"),
        ("Workforce Analyst",     f"CALL `hive_mind_core.analyze_workforce_patterns`({batch})"),
    ]

    print(f"🚀 HiveMind Agent Runner")
    print(f"   Batch size: {batch} | Max retries: {args.retries} | Cooldown: {args.cooldown}s")
    print(f"   Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = {}
    for name, query in agents:
        success = run_agent(client, name, query, max_retries=args.retries)
        results[name] = success
        
        if success:
            print(f"   Cooling down {args.cooldown}s before next agent...")
            time.sleep(args.cooldown)

    # Final report
    print("\n" + "=" * 60)
    print("📊 Final Report")
    print("=" * 60)

    tables = [
        ('fact_work_patterns', 'Workforce Patterns'),
        ('support_thread_scores', 'Support Thread Scores'),
        ('fact_questions', 'Extracted Questions'),
        ('sales_leads', 'Sales Leads'),
        ('dim_user_attributes', 'User Profiles'),
    ]
    
    for table, label in tables:
        try:
            for row in client.query(f"SELECT count(*) as cnt FROM `augos-core-data.hive_mind_core.{table}`").result():
                print(f"   {label}: {row.cnt} rows")
        except Exception as e:
            print(f"   {label}: Error - {e}")

    print("\n" + "=" * 60)
    for name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"   {status} — {name}")
    print("=" * 60)


if __name__ == "__main__":
    main()
