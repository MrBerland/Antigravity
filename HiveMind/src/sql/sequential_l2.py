"""
sequential_l2.py — Sequential wave classifier
Runs 5,000-email batches one at a time so BQ slot allocation is efficient.
Appends progress to /tmp/hivemind_pipeline.log and stdout.
"""
import os, time

os.environ.setdefault(
    "GOOGLE_APPLICATION_CREDENTIALS",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "credentials", "hive-mind-admin.json"))
)

from google.cloud import bigquery

PROJECT = "augos-core-data"
DATASET = "hive_mind_core"
LOG     = "/tmp/hivemind_pipeline.log"

client = bigquery.Client(project=PROJECT)


def log(msg):
    ts   = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def count(status):
    sql  = f"SELECT COUNT(*) AS n FROM `{PROJECT}.{DATASET}.staging_raw_emails` WHERE processing_status = '{status}'"
    rows = list(client.query(sql, location="US").result(timeout=60))
    return rows[0]["n"]


# ── Prompt is plain text — no double-quotes inside SQL single-quoted strings ──
# We embed the verdict list and instructions using only single-quote-safe chars.
BATCH_SQL = (
    "CREATE TEMP TABLE pending_ai AS\n"
    "SELECT message_id, sender, subject, snippet\n"
    f"FROM `{PROJECT}.{DATASET}.staging_raw_emails`\n"
    "WHERE processing_status = 'PENDING'\n"
    "  AND ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)\n"
    "LIMIT 5000;\n\n"
    "CREATE TEMP TABLE ai_results AS\n"
    "SELECT message_id, ml_generate_text_llm_result AS raw\n"
    "FROM ML.GENERATE_TEXT(\n"
    f"  MODEL `{PROJECT}.{DATASET}.gemini_flash`,\n"
    "  (SELECT message_id,\n"
    "    CONCAT(\n"
    "      'Email privacy classifier. Reply with only a JSON object, no markdown. ',\n"
    "      'Choose ONE verdict from: BUSINESS PERSONAL HR_SENSITIVE CONFIDENTIAL MARKETING SYSTEM. ',\n"
    "      'BUSINESS=work ops client deal invoice. ',\n"
    "      'PERSONAL=private family finance health shopping travel banking. ',\n"
    "      'HR_SENSITIVE=salary payroll medical leave performance. ',\n"
    "      'CONFIDENTIAL=legal board NDA contract acquisition. ',\n"
    "      'MARKETING=newsletter promo unsolicited advert. ',\n"
    "      'SYSTEM=automated alert notification receipt delivery. ',\n"
    "      'Reply JSON with fields verdict confidence reason. ',\n"
    "      'From: ', sender, ' Subject: ', subject, ' Preview: ', snippet\n"
    "    ) AS prompt\n"
    "  FROM pending_ai),\n"
    "  STRUCT(0.1 AS temperature, 100 AS max_output_tokens, TRUE AS flatten_json_output));\n\n"
    f"UPDATE `{PROJECT}.{DATASET}.staging_raw_emails` e\n"
    "SET security_verdict = JSON_VALUE(r.raw, '$.verdict'),\n"
    "    ai_category = CONCAT('AI_L2:', COALESCE(JSON_VALUE(r.raw, '$.reason'), 'ok')),\n"
    "    processing_status = 'CLASSIFIED_L2'\n"
    "FROM ai_results r\n"
    "WHERE e.message_id = r.message_id\n"
    "  AND JSON_VALUE(r.raw, '$.verdict') IS NOT NULL;\n\n"
    f"UPDATE `{PROJECT}.{DATASET}.staging_raw_emails` e\n"
    "SET security_verdict = 'BUSINESS',\n"
    "    ai_category = 'AI_L2_PARSE_FAIL',\n"
    "    processing_status = 'CLASSIFIED_L2'\n"
    "FROM ai_results r\n"
    "WHERE e.message_id = r.message_id\n"
    "  AND JSON_VALUE(r.raw, '$.verdict') IS NULL;\n"
)


if __name__ == "__main__":
    log("=== Sequential L2 batcher starting (5,000 emails/wave) ===")
    wave = 0
    while True:
        n_pending = count("PENDING")
        if n_pending == 0:
            log(f"All classified! Total L2: {count('CLASSIFIED_L2'):,}")
            break

        wave += 1
        log(f"Wave {wave}: {n_pending:,} pending — submitting batch...")
        try:
            job = client.query(BATCH_SQL, location="US")
            job.result(timeout=900)
            log(f"  Wave {wave} done. L2 total: {count('CLASSIFIED_L2'):,}")
        except Exception as exc:
            log(f"  Wave {wave} error: {exc}")
            time.sleep(30)

        time.sleep(3)
