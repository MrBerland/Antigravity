"""
hivemind_pipeline.py
====================
Complete HiveMind pipeline orchestrator. Runs entirely in the background.
Your machine is free as soon as this is launched.

Pipeline stages (in order):
  1. Submit ALL Layer 2 AI classification jobs to BigQuery (fire-and-forget)
  2. Poll every 5 min until all emails are classified
  3. Generate embeddings for the full corpus
  4. Run all AI agents (Support KB, Sales leads, Workforce analysis)
  5. Email tim@augos.io with a full completion report

Launch and walk away:
    nohup python3 HiveMind/hivemind_pipeline.py > /tmp/hivemind_pipeline.log 2>&1 &
    echo "Running as PID $!"

Check progress any time:
    tail -f /tmp/hivemind_pipeline.log

Or check BQ directly:
    python3 HiveMind/src/sql/submit_l2_jobs.py --status
"""

import os
import sys
import time
import base64
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── Config ─────────────────────────────────────────────────────────────────────
_ROOT = os.path.dirname(os.path.abspath(__file__))
SA_FILE = os.path.join(_ROOT, "credentials", "hive-mind-admin.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_FILE

PROJECT   = "augos-core-data"
DATASET   = "hive_mind_core"
NOTIFY_TO = "tim@augos.io"
TABLE     = f"`{PROJECT}.{DATASET}.staging_raw_emails`"
MODEL     = f"`{PROJECT}.{DATASET}.gemini_flash`"
EMBED_MODEL = f"`{PROJECT}.{DATASET}.embedding_model`"

BUFFER_GUARD = "AND ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)"
POLL_INTERVAL = 300  # 5 minutes between checks

from google.cloud import bigquery
from google.oauth2 import service_account
from googleapiclient.discovery import build

bq_client = bigquery.Client(project=PROJECT)

# ── Logging ────────────────────────────────────────────────────────────────────
def log(msg: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[{ts}] {msg}", flush=True)


# ── BigQuery helpers ────────────────────────────────────────────────────────────
def bq_query(sql: str, timeout: int = 120) -> list:
    job = bq_client.query(sql, location="US")
    return list(job.result(timeout=timeout))


def bq_submit(sql: str) -> str:
    """Submit a job non-blocking. Returns job_id."""
    job = bq_client.query(sql, location="US")
    return job.job_id


def get_counts() -> dict:
    rows = bq_query(
        f"SELECT processing_status, COUNT(*) as n FROM {TABLE} GROUP BY 1",
        timeout=60
    )
    return {r["processing_status"]: r["n"] for r in rows}


def get_running_l2_jobs() -> list:
    jobs = list(bq_client.list_jobs(max_results=500, state_filter="RUNNING"))
    return [j for j in jobs if "pending_ai" in (getattr(j, "query", "") or "").lower()]


# ── Stage 1: Layer 2 classification ────────────────────────────────────────────
L2_BATCH_SQL = f"""
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
      'Privacy classifier for corporate email. ONE category only. JSON only.\\n',
      'BUSINESS=work/client/ops, PERSONAL=private/family/finances/health, ',
      'HR_SENSITIVE=salary/HR/medical, CONFIDENTIAL=legal/board/NDA, ',
      'MARKETING=newsletter/promo(unsolicited), SYSTEM=automated/alert/notification\\n',
      'From:', sender, ' Subject:', subject, ' Preview:', snippet, '\\n',
      'JSON: {{"verdict":"CATEGORY","confidence":0.9,"reason":"one line"}}'
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


def stage1_submit_l2():
    log("=== STAGE 1: Layer 2 AI Classification ===")
    counts = get_counts()
    pending = counts.get("PENDING", 0)
    already_running = get_running_l2_jobs()

    log(f"  PENDING: {pending:,}  |  Already running BQ jobs: {len(already_running)}")

    if pending == 0:
        log("  Nothing to classify. Skipping L2.")
        return 0

    # How many new batches to submit
    covered  = len(already_running) * 1000
    needed   = max(0, pending - covered)
    to_submit = (needed + 999) // 1000

    if to_submit <= 0:
        log(f"  {len(already_running)} jobs already cover all {pending:,} PENDING emails.")
        return len(already_running)

    log(f"  Submitting {to_submit} new batch jobs ({to_submit * 1000:,} emails, ~${to_submit * 0.03:.2f})")

    submitted = 0
    for i in range(to_submit):
        try:
            job_id = bq_submit(L2_BATCH_SQL)
            submitted += 1
            if (i + 1) % 25 == 0:
                log(f"  ... {i+1}/{to_submit} submitted")
            time.sleep(0.3)
        except Exception as e:
            log(f"  ⚠️  Submit error at batch {i+1}: {e}")
            time.sleep(5)

    log(f"  ✅ {submitted + len(already_running)} total jobs in flight. Machine is free.")
    return submitted + len(already_running)


def wait_for_l2():
    log("  Polling until all emails classified (every 5 min)...")
    while True:
        counts = get_counts()
        pending = counts.get("PENDING", 0)
        classified_l2 = counts.get("CLASSIFIED_L2", 0)
        running = get_running_l2_jobs()

        log(f"  PENDING: {pending:,}  |  CLASSIFIED_L2: {classified_l2:,}  |  Jobs running: {len(running)}")

        if pending == 0:
            log("  ✅ All emails classified!")
            return counts

        if pending > 0 and len(running) == 0:
            log(f"  ⚠️  {pending:,} still pending but no jobs running — submitting more...")
            stage1_submit_l2()

        time.sleep(POLL_INTERVAL)


# ── Stage 2: Embeddings ─────────────────────────────────────────────────────────
EMBED_SQL = f"""
CREATE TEMP TABLE to_embed AS
SELECT message_id, CONCAT('Subject: ', subject, ' From: ', sender, ' ', snippet) AS content
FROM {TABLE}
WHERE security_verdict = 'BUSINESS'
  AND message_id NOT IN (SELECT message_id FROM `{PROJECT}.{DATASET}.fact_embeddings`)
LIMIT 2000;

INSERT INTO `{PROJECT}.{DATASET}.fact_embeddings` (message_id, embedding, embedded_at)
SELECT t.message_id, e.ml_generate_embedding_result AS embedding, CURRENT_TIMESTAMP()
FROM ML.GENERATE_EMBEDDING(
  MODEL {EMBED_MODEL},
  (SELECT message_id, content AS content FROM to_embed),
  STRUCT(TRUE AS flatten_json_output)
) e
JOIN to_embed t ON t.message_id = e.message_id;
"""


def stage2_embeddings():
    log("=== STAGE 2: Generating Embeddings ===")
    try:
        rows = bq_query(
            f"SELECT COUNT(*) as n FROM `{PROJECT}.{DATASET}.fact_embeddings`", timeout=30
        )
        existing = rows[0]["n"] if rows else 0
    except Exception:
        existing = 0

    business_rows = bq_query(
        f"SELECT COUNT(*) as n FROM {TABLE} WHERE security_verdict = 'BUSINESS'", timeout=60
    )
    business_count = business_rows[0]["n"] if business_rows else 0
    to_embed = max(0, business_count - existing)

    log(f"  Business emails: {business_count:,}  |  Already embedded: {existing:,}  |  To embed: {to_embed:,}")

    if to_embed == 0:
        log("  Nothing to embed. Skipping.")
        return existing

    # Submit in batches of 2000
    batches = (to_embed + 1999) // 2000
    log(f"  Submitting {batches} embedding batches (~${to_embed * 0.000005:.2f})")
    jobs = []
    for _ in range(batches):
        try:
            jid = bq_submit(EMBED_SQL)
            jobs.append(jid)
            time.sleep(1)
        except Exception as e:
            log(f"  ⚠️  Embed submit error: {e}")

    # Wait for embedding jobs
    log(f"  Waiting for {len(jobs)} embedding jobs...")
    for jid in jobs:
        j = bq_client.get_job(jid, location="US")
        while j.state == "RUNNING":
            time.sleep(30)
            j.reload()
        if j.errors:
            log(f"  ⚠️  Embedding job {jid[:16]} error: {j.errors}")

    rows = bq_query(
        f"SELECT COUNT(*) as n FROM `{PROJECT}.{DATASET}.fact_embeddings`", timeout=30
    )
    final = rows[0]["n"] if rows else 0
    log(f"  ✅ Embeddings complete. Total: {final:,}")
    return final


# ── Stage 3: AI Agents ──────────────────────────────────────────────────────────
AGENTS = [
    ("Support Thread Scorer",
     f"CALL `{PROJECT}.{DATASET}.analyze_support_threads`(200)"),
    ("Question Extractor",
     f"CALL `{PROJECT}.{DATASET}.analyze_questions`(200)"),
    ("Sales Lead Scorer",
     f"CALL `{PROJECT}.{DATASET}.analyze_sales_leads`(200)"),
    ("Workforce Analyst",
     f"CALL `{PROJECT}.{DATASET}.analyze_workforce_patterns`(200)"),
]


def stage3_agents() -> dict:
    log("=== STAGE 3: Running AI Agents ===")
    results = {}
    for name, sql in AGENTS:
        log(f"  Running: {name}")
        try:
            job = bq_client.query(sql, location="US")
            job.result(timeout=1200)  # 20 min per agent
            results[name] = "✅ Success"
            log(f"  ✅ {name} complete")
        except Exception as e:
            results[name] = f"⚠️ {str(e)[:80]}"
            log(f"  ⚠️  {name} error: {e}")
        time.sleep(30)  # brief cool-down between agents
    return results


# ── Stage 4: Email notification ─────────────────────────────────────────────────
def send_completion_email(final_counts: dict, agent_results: dict,
                          embed_count: int, elapsed_min: int):
    log("=== STAGE 4: Sending completion email ===")
    try:
        creds = service_account.Credentials.from_service_account_file(
            SA_FILE,
            scopes=["https://www.googleapis.com/auth/gmail.send"]
        )
        creds = creds.with_subject(NOTIFY_TO)
        gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)

        total = sum(final_counts.values())
        business = final_counts.get("CLASSIFIED_L2", 0) + final_counts.get("CLASSIFIED_L1", 0)

        rows_html = "\n".join(
            f"<tr><td>{k}</td><td align='right'>{v:,}</td></tr>"
            for k, v in sorted(final_counts.items(), key=lambda x: -x[1])
        )
        agent_html = "\n".join(
            f"<tr><td>{name}</td><td>{status}</td></tr>"
            for name, status in agent_results.items()
        )

        html = f"""
<html><body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
<h2 style="color:#1a73e8">🧠 HiveMind Pipeline Complete</h2>
<p>All processes finished in <strong>{elapsed_min} minutes</strong>.</p>

<h3>Classification Results</h3>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%">
<tr style="background:#1a73e8;color:white"><th>Status</th><th>Count</th></tr>
{rows_html}
<tr style="background:#f5f5f5;font-weight:bold"><td>Total</td><td align="right">{total:,}</td></tr>
</table>

<h3>AI Agents</h3>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%">
<tr style="background:#1a73e8;color:white"><th>Agent</th><th>Result</th></tr>
{agent_html}
</table>

<h3>Embeddings</h3>
<p>{embed_count:,} business emails embedded for semantic search.</p>

<h3>Next Steps</h3>
<ul>
<li>Open the HiveMind UI: <code>cd hive-mind-ui && npm run dev</code></li>
<li>View the Knowledge Base — support threads and questions are ready</li>
<li>Review sales leads in the Sales Intelligence section</li>
<li>Check Workforce Patterns dashboard</li>
<li>Gmail watch expires <strong>12 March 2026</strong> — renew with:<br>
    <code>python3 HiveMind/activate_watch_all_users.py</code></li>
</ul>

<p style="color:#666;font-size:12px">HiveMind · augos-core-data · {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>
</body></html>
"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"✅ HiveMind Pipeline Complete — {total:,} emails classified"
        msg["From"]    = NOTIFY_TO
        msg["To"]      = NOTIFY_TO
        msg.attach(MIMEText(html, "html"))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        gmail.users().messages().send(userId="me", body={"raw": raw}).execute()
        log(f"  ✅ Email sent to {NOTIFY_TO}")
    except Exception as e:
        log(f"  ⚠️  Email failed: {e}")


# ── Main ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    t_start = time.time()
    log("🚀 HiveMind Pipeline starting")
    log(f"   Project: {PROJECT}")
    log(f"   Notify:  {NOTIFY_TO}")
    log("")

    # Stage 1 — submit L2 jobs + wait
    stage1_submit_l2()
    final_counts = wait_for_l2()

    # Stage 2 — embeddings
    embed_count = stage2_embeddings()

    # Stage 3 — agents
    agent_results = stage3_agents()

    # Stage 4 — email
    elapsed = int((time.time() - t_start) / 60)
    send_completion_email(final_counts, agent_results, embed_count, elapsed)

    log(f"\n🏁 Pipeline complete in {elapsed} minutes.")
