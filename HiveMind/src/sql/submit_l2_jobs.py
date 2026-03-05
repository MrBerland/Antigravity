"""
submit_l2_jobs.py
=================
Submits ALL Layer 2 AI classification batches as independent BigQuery jobs
and then EXITS. Your machine is free immediately.

Jobs run entirely in Google Cloud — no local process needed.
Each job classifies 1,000 emails via ML.GENERATE_TEXT (Gemini Flash).
Results write directly back to BigQuery when each job completes.

Usage:
    python3 HiveMind/src/sql/submit_l2_jobs.py

After running, check progress any time with:
    python3 HiveMind/src/sql/submit_l2_jobs.py --status
"""

import os
import sys
import time
import argparse

os.environ.setdefault(
    "GOOGLE_APPLICATION_CREDENTIALS",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "credentials", "hive-mind-admin.json"))
)

from google.cloud import bigquery

PROJECT = "augos-core-data"
DATASET = "hive_mind_core"
TABLE   = f"`{PROJECT}.{DATASET}.staging_raw_emails`"
MODEL   = f"`{PROJECT}.{DATASET}.gemini_flash`"

# Buffer guard: skip rows ingested in the last 2 hours (streaming buffer restriction)
BUFFER_GUARD = "AND ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)"

BATCH_SQL = f"""
CREATE TEMP TABLE pending_ai AS
SELECT message_id, sender, subject, snippet
FROM {TABLE}
WHERE processing_status = 'PENDING' {BUFFER_GUARD}
LIMIT 1000;

CREATE TEMP TABLE ai_results AS
SELECT message_id, ml_generate_text_llm_result AS raw
FROM ML.GENERATE_TEXT(
  MODEL {MODEL},
  (SELECT message_id,
    CONCAT(
      'Privacy classifier for corporate email. ONE category only. JSON only, no markdown.\\n',
      'BUSINESS=work/client/ops, PERSONAL=private/family/finances/health, ',
      'HR_SENSITIVE=salary/HR/medical, CONFIDENTIAL=legal/board/NDA, ',
      'MARKETING=newsletter/promo(unsolicited), SYSTEM=automated/alert/notification\\n',
      'From:', sender, ' Subject:', subject, ' Preview:', snippet, '\\n',
      'JSON: {{"verdict":"CATEGORY","confidence":0.9,"reason":"brief"}}'
    ) AS prompt
  FROM pending_ai),
  STRUCT(0.1 AS temperature, 100 AS max_output_tokens, TRUE AS flatten_json_output));

UPDATE {TABLE} e
SET security_verdict = JSON_VALUE(r.raw, '$.verdict'),
    ai_category = CONCAT('AI_L2:', COALESCE(JSON_VALUE(r.raw, '$.reason'), 'ok')),
    processing_status = 'CLASSIFIED_L2'
FROM ai_results r
WHERE e.message_id = r.message_id
  AND JSON_VALUE(r.raw, '$.verdict') IS NOT NULL;

UPDATE {TABLE} e
SET security_verdict = 'BUSINESS', ai_category = 'AI_L2_PARSE_FAIL',
    processing_status = 'CLASSIFIED_L2'
FROM ai_results r
WHERE e.message_id = r.message_id
  AND JSON_VALUE(r.raw, '$.verdict') IS NULL;
"""

client = bigquery.Client(project=PROJECT)


def get_counts():
    sql = f"""
    SELECT processing_status, COUNT(*) as n
    FROM {TABLE}
    GROUP BY 1 ORDER BY n DESC
    """
    job = client.query(sql, location="US")
    return {r["processing_status"]: r["n"] for r in job.result(timeout=60)}


def get_running_l2_jobs():
    jobs = list(client.list_jobs(max_results=500, state_filter="RUNNING"))
    return [j for j in jobs if "pending_ai" in (getattr(j, "query", "") or "").lower()]


def submit_jobs():
    # Check current state
    print("\n📊 Current state:")
    counts = get_counts()
    pending = counts.get("PENDING", 0)
    classified_l2 = counts.get("CLASSIFIED_L2", 0)
    classified_l1 = counts.get("CLASSIFIED_L1", 0)
    allow = counts.get("ALLOW", 0)
    print(f"  PENDING (needs AI):     {pending:>10,}")
    print(f"  CLASSIFIED_L1 (domain): {classified_l1:>10,}")
    print(f"  CLASSIFIED_L2 (AI):     {classified_l2:>10,}")
    print(f"  ALLOW (pre-existing):   {allow:>10,}")

    if pending == 0:
        print("\n✅ Nothing to classify! All emails are processed.")
        return

    # Count how many L2 jobs are already running
    running = get_running_l2_jobs()
    print(f"\n  Already running BQ jobs: {len(running)}")

    # Calculate how many new batches to submit
    # Each batch does 1,000. Subtract already-running batches.
    emails_to_classify = pending - (len(running) * 1000)
    if emails_to_classify <= 0:
        print(f"\n  ⏳ {len(running)} jobs already in flight covering all {pending:,} PENDING emails.")
        print(f"     Check --status in a while to see results.\n")
        return

    batches_needed = max(0, (emails_to_classify + 999) // 1000)
    # Cap at 400 concurrent jobs (BQ project quota is usually higher but be conservative)
    batches_to_submit = min(batches_needed, 400 - len(running))

    print(f"\n🚀 Submitting {batches_to_submit} batch jobs ({batches_to_submit * 1000:,} emails)")
    print(f"   Estimated cost: ~${batches_to_submit * 0.03:.2f}")
    print(f"   Jobs run in Google Cloud — your machine is free to go.\n")

    submitted = []
    for i in range(batches_to_submit):
        job = client.query(BATCH_SQL, location="US")  # non-blocking — fire and forget
        submitted.append(job.job_id)
        if (i + 1) % 10 == 0 or i == batches_to_submit - 1:
            print(f"  Submitted {i+1}/{batches_to_submit} jobs...", flush=True)
        # Tiny pause to avoid overwhelming the submission API
        time.sleep(0.3)

    print(f"\n✅ All {len(submitted)} jobs submitted.")
    print(f"   First job: {submitted[0]}")
    print(f"   Last job:  {submitted[-1]}")
    print(f"\n   Jobs are running in BigQuery. Your machine is free.")
    print(f"   Check progress: python3 HiveMind/src/sql/submit_l2_jobs.py --status\n")

    # Save job IDs for monitoring
    log_path = os.path.join(os.path.dirname(__file__), "l2_job_ids.txt")
    with open(log_path, "w") as f:
        f.write("\n".join(submitted))
    print(f"   Job IDs saved to: {log_path}")


def show_status():
    print("\n📊 HiveMind Classification Status\n")

    counts = get_counts()
    total = sum(counts.values())
    for status, n in sorted(counts.items(), key=lambda x: -x[1]):
        pct = n * 100 / total if total else 0
        bar = "█" * int(pct / 2)
        print(f"  {status:<20} {n:>10,}  {pct:>5.1f}%  {bar}")

    print(f"\n  Total emails: {total:,}")

    # Running L2 jobs
    running = get_running_l2_jobs()
    print(f"\n  BQ Layer 2 jobs running: {len(running)}")

    pending = counts.get("PENDING", 0)
    classified_l2 = counts.get("CLASSIFIED_L2", 0)
    if classified_l2 > 0:
        pct_done = classified_l2 * 100 / (classified_l2 + pending) if (classified_l2 + pending) > 0 else 0
        print(f"  L2 progress: {classified_l2:,} done / {classified_l2 + pending:,} ({pct_done:.1f}%)")

    if pending == 0:
        print("\n  🎉 All emails classified! Ready to run agents.")
    elif len(running) > 0:
        print(f"\n  ⏳ {len(running)} jobs in flight. Check back in ~10 minutes.")
    else:
        print(f"\n  ⚠️  {pending:,} PENDING but no jobs running.")
        print(f"     Run: python3 HiveMind/src/sql/submit_l2_jobs.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit Layer 2 BQ classification jobs")
    parser.add_argument("--status", action="store_true", help="Show classification progress")
    args = parser.parse_args()

    if args.status:
        show_status()
    else:
        submit_jobs()
