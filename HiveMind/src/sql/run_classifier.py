"""
run_classifier.py
=================
Deploys and runs the two-layer personal email classifier against the
HiveMind staging table.

Usage:
    # 1. Deploy procedures and views (run once):
    python3 run_classifier.py --deploy

    # 2. Run Layer 1 (domain rules — instant, free):
    python3 run_classifier.py --layer1

    # 3. Run Layer 2 AI classifier in batches (costs Gemini tokens):
    python3 run_classifier.py --layer2 --batch 1000 --loops 50

    # 4. See classification summary:
    python3 run_classifier.py --summary

    # 5. See what got flagged as personal (subject lines only):
    python3 run_classifier.py --personal-audit

    # 6. Full run (deploy + l1 + l2):
    python3 run_classifier.py --deploy --layer1 --layer2 --batch 500 --loops 200
"""

import argparse
import os
import sys
import time
from google.cloud import bigquery

# ── Config ────────────────────────────────────────────────────────────────────
PROJECT_ID   = "augos-core-data"
DATASET_ID   = "hive_mind_core"
SQL_DIR      = os.path.join(os.path.dirname(__file__), "..", "sql")
SA_FILE      = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "HiveMind", "credentials", "hive-mind-admin.json")
)

os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", SA_FILE)
client = bigquery.Client(project=PROJECT_ID)

# ── Governance seed data ─────────────────────────────────────────────────────
GOVERNANCE_RULES = [
    # (rule_type, match_type, pattern, notes)
    # Personal consumer email providers
    ('PERSONAL', 'DOMAIN_WILDCARD', 'gmail.com',          'Personal gmail accounts'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'googlemail.com',     'Personal gmail EU variant'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'yahoo.com',          'Personal Yahoo'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'yahoo.co.uk',        'Personal Yahoo UK'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'yahoo.co.za',        'Personal Yahoo ZA'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'hotmail.com',        'Personal Hotmail'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'hotmail.co.uk',      'Personal Hotmail UK'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'outlook.com',        'Personal Outlook'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'live.com',           'Personal Microsoft Live'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'msn.com',            'Personal MSN'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'icloud.com',         'Personal Apple iCloud'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'me.com',             'Personal Apple Me'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'mac.com',            'Personal Apple Mac'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'protonmail.com',     'Personal ProtonMail'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'proton.me',          'Personal Proton'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'aol.com',            'Personal AOL'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'webmail.co.za',      'Personal ZA Webmail'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'telkomsa.net',       'Personal Telkom SA'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'vodamail.co.za',     'Personal Vodacom Mail'),
    ('PERSONAL', 'DOMAIN_WILDCARD', 'iafrica.com',        'Personal iAfrica'),
    # Marketing
    ('MARKETING', 'DOMAIN_WILDCARD', 'mailchimp.com',     'Mailchimp campaigns'),
    ('MARKETING', 'DOMAIN_WILDCARD', 'hubspot.com',       'HubSpot marketing'),
    ('MARKETING', 'DOMAIN_WILDCARD', 'sendgrid.net',      'SendGrid bulk mail'),
    ('MARKETING', 'DOMAIN_WILDCARD', 'klaviyo.com',       'Klaviyo ecomm email'),
    ('MARKETING', 'DOMAIN_WILDCARD', 'constantcontact.com', 'Constant Contact'),
    ('MARKETING', 'DOMAIN_WILDCARD', 'campaign-monitor.com', 'Campaign Monitor'),
    ('MARKETING', 'DOMAIN_WILDCARD', 'marketing.tajhotels.com', 'Taj Hotels marketing'),
    # System
    ('SYSTEM', 'DOMAIN_WILDCARD', 'zohocalendar.com',    'Zoho Calendar notifications'),
    ('SYSTEM', 'EXACT_EMAIL',     'noreply@google.com',  'Google noreply'),
    ('SYSTEM', 'EXACT_EMAIL',     'no-reply@accounts.google.com', 'Google account alerts'),
    ('SYSTEM', 'DOMAIN_WILDCARD', 'notifications.google.com', 'Google notifications'),
    ('SYSTEM', 'EXACT_EMAIL',     'noreply@github.com',  'GitHub notifications'),
    ('SYSTEM', 'DOMAIN_WILDCARD', 'jira.atlassian.com',  'Jira notifications'),
    ('SYSTEM', 'DOMAIN_WILDCARD', 'slack.com',           'Slack notification emails'),
    ('SYSTEM', 'DOMAIN_WILDCARD', 'zoom.us',             'Zoom meeting notifications'),
    # Allow internal
    ('ALLOW', 'DOMAIN_WILDCARD', 'augos.io',             'Internal Augos domain'),
]


# ── SQL constants for procedures and views ────────────────────────────────────

LAYER1_PROC_SQL = """
CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.layer1_domain_classify`()
BEGIN
  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET security_verdict = 'PERSONAL', processing_status = 'CLASSIFIED_L1'
  WHERE e.processing_status = 'PENDING'
    AND EXISTS (SELECT 1 FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
      WHERE r.rule_type = 'PERSONAL' AND (
        (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))
        OR (r.match_type = 'EXACT_EMAIL' AND LOWER(e.sender) = LOWER(r.pattern))));

  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET security_verdict = 'MARKETING', processing_status = 'CLASSIFIED_L1'
  WHERE e.processing_status = 'PENDING'
    AND EXISTS (SELECT 1 FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
      WHERE r.rule_type = 'MARKETING' AND (
        (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))
        OR (r.match_type = 'EXACT_EMAIL' AND LOWER(e.sender) = LOWER(r.pattern))));

  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET security_verdict = 'SYSTEM', processing_status = 'CLASSIFIED_L1'
  WHERE e.processing_status = 'PENDING'
    AND EXISTS (SELECT 1 FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
      WHERE r.rule_type = 'SYSTEM' AND (
        (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))
        OR (r.match_type = 'EXACT_EMAIL' AND LOWER(e.sender) = LOWER(r.pattern))));

  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET security_verdict = 'BUSINESS', processing_status = 'CLASSIFIED_L1'
  WHERE e.processing_status = 'PENDING'
    AND EXISTS (SELECT 1 FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
      WHERE r.rule_type = 'ALLOW' AND (
        (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))
        OR (r.match_type = 'EXACT_EMAIL' AND LOWER(e.sender) = LOWER(r.pattern))));

  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails`
  SET security_verdict = 'PERSONAL', ai_category = 'SUBJECT_PATTERN_MATCH', processing_status = 'CLASSIFIED_L1'
  WHERE processing_status = 'PENDING'
    AND REGEXP_CONTAINS(LOWER(subject), r'\\b(unsubscribe|newsletter|your order|shipment|delivery|tracking number|your account|password reset|verify your email|confirm your email|receipt|bank statement|statement of account|loan|insurance|medical aid|discovery health|momentum|liberty|old mutual|fnb|nedbank|absa|standard bank|capitec|nedgroup)\\b');

  SELECT CONCAT(
    'Layer 1 complete. ',
    CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE security_verdict = 'PERSONAL'  AND processing_status = 'CLASSIFIED_L1') AS STRING), ' PERSONAL, ',
    CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE security_verdict = 'MARKETING' AND processing_status = 'CLASSIFIED_L1') AS STRING), ' MARKETING, ',
    CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE security_verdict = 'SYSTEM'    AND processing_status = 'CLASSIFIED_L1') AS STRING), ' SYSTEM, ',
    CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE security_verdict = 'BUSINESS'  AND processing_status = 'CLASSIFIED_L1') AS STRING), ' BUSINESS tagged.'
  ) AS status;
END
"""

LAYER2_PROC_SQL = """
CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.layer2_ai_classify`(batch_size INT64)
BEGIN
  CREATE TEMP TABLE pending_ai_classify AS
  SELECT message_id, sender, subject, snippet
  FROM `augos-core-data.hive_mind_core.staging_raw_emails`
  WHERE processing_status = 'PENDING'
  LIMIT batch_size;

  CREATE TEMP TABLE ai_verdicts AS
  SELECT message_id, sender, ml_generate_text_llm_result AS raw_response
  FROM ML.GENERATE_TEXT(
    MODEL `augos-core-data.hive_mind_core.gemini_flash`,
    (SELECT message_id, sender,
      CONCAT(
        'You are a privacy classifier for a corporate email system. ',
        'Classify this email into EXACTLY ONE category. Return ONLY a JSON object, no markdown, no explanation.\\n\\n',
        'CATEGORIES:\\n',
        '  BUSINESS     - Work-related: client communication, contracts, operations, support tickets, projects\\n',
        '  PERSONAL     - Private life: family, friends, personal finances, health, hobbies, shopping\\n',
        '  HR_SENSITIVE - Salary, disciplinary action, resignation, recruitment, medical leave, benefits\\n',
        '  CONFIDENTIAL - Legal matters, board communications, investor relations, NDA content\\n',
        '  MARKETING    - Newsletter, promotion, discount offer, event invitation (unsolicited)\\n',
        '  SYSTEM       - Automated notification: alerts, calendar invite, account confirmation\\n\\n',
        'EMAIL:\\nFrom: ', sender, '\\nSubject: ', subject, '\\nPreview: ', snippet, '\\n\\n',
        'RESPOND WITH JSON ONLY:\\n',
        '{\"verdict\": \"CATEGORY\", \"confidence\": 0.0, \"reason\": \"one sentence\"}'
      ) AS prompt
    FROM pending_ai_classify),
    STRUCT(0.1 AS temperature, 150 AS max_output_tokens, TRUE AS flatten_json_output));

  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET security_verdict = JSON_VALUE(v.raw_response, '$.verdict'),
      ai_category = CONCAT('AI_L2:', JSON_VALUE(v.raw_response, '$.reason')),
      processing_status = 'CLASSIFIED_L2'
  FROM ai_verdicts v
  WHERE e.message_id = v.message_id AND JSON_VALUE(v.raw_response, '$.verdict') IS NOT NULL;

  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET security_verdict = 'BUSINESS', ai_category = 'AI_L2_PARSE_FAILURE', processing_status = 'CLASSIFIED_L2'
  FROM ai_verdicts v
  WHERE e.message_id = v.message_id AND JSON_VALUE(v.raw_response, '$.verdict') IS NULL;

  SELECT CONCAT(
    'Layer 2 AI classify complete. Batch of ',
    CAST((SELECT COUNT(*) FROM pending_ai_classify) AS STRING),
    ' emails. Remaining PENDING: ',
    CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE processing_status = 'PENDING') AS STRING)
  ) AS status;
END
"""

VIEWS_SQL = {
    "v_classification_summary": """
        CREATE OR REPLACE VIEW `augos-core-data.hive_mind_core.v_classification_summary` AS
        SELECT
          security_verdict, processing_status,
          COUNT(*) AS email_count,
          ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct_of_total,
          MIN(timestamp) AS earliest, MAX(timestamp) AS latest,
          COUNT(DISTINCT REGEXP_EXTRACT(sender, r'@(.+)$')) AS distinct_sender_domains
        FROM `augos-core-data.hive_mind_core.staging_raw_emails`
        GROUP BY 1, 2 ORDER BY email_count DESC
    """,
    "v_business_emails": """
        CREATE OR REPLACE VIEW `augos-core-data.hive_mind_core.v_business_emails` AS
        SELECT * FROM `augos-core-data.hive_mind_core.staging_raw_emails`
        WHERE security_verdict = 'BUSINESS'
          AND processing_status IN ('CLASSIFIED_L1', 'CLASSIFIED_L2')
    """,
    "v_personal_flagged": """
        CREATE OR REPLACE VIEW `augos-core-data.hive_mind_core.v_personal_flagged` AS
        SELECT message_id, thread_id, timestamp, sender, subject,
               security_verdict, ai_category, processing_status, raw_gcs_uri
        FROM `augos-core-data.hive_mind_core.staging_raw_emails`
        WHERE security_verdict IN ('PERSONAL', 'HR_SENSITIVE', 'CONFIDENTIAL')
    """,
}


# ── Helper ────────────────────────────────────────────────────────────────────

def run_query(sql: str, description: str = "") -> list:
    """Run a SELECT query with a 30-min timeout. Returns list of rows."""
    print(f"  \u25b6 {description or sql[:80]}")
    job = client.query(sql, location="US")
    result = job.result(timeout=1800)  # blocks until done or times out
    return list(result)


def run_statement(sql: str, description: str):
    """Run a DML/DDL/scripting statement. Waits up to 30 min. Prints elapsed time."""
    print(f"  \u25b6 {description}")
    t0 = time.time()
    job = client.query(sql, location="US")
    job.result(timeout=1800)  # blocks until done; raises on error
    elapsed = int(time.time() - t0)
    print(f"  \u2713 Done ({elapsed}s)")


def pending_count() -> int:
    """Fast direct count of fully committed PENDING emails."""
    job = client.query(
        "SELECT COUNT(*) as n FROM `augos-core-data.hive_mind_core.staging_raw_emails` "
        "WHERE processing_status = 'PENDING'",
        location="US"
    )
    rows = list(job.result(timeout=120))
    return rows[0]["n"] if rows else 0


# ── Commands ──────────────────────────────────────────────────────────────────

def deploy():
    """Seed governance rules, then deploy procedures and views as separate statements."""
    print("\n📦 Step 1: Seeding governance rules...")
    # Use streaming insert for the seed data — avoids complex multi-statement scripting
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.dim_governance_rules"
    
    # First, check what already exists
    existing = run_query(
        f"SELECT pattern, rule_type FROM `{table_ref}` WHERE added_by = 'pii_classifier'",
        "Checking existing rules"
    )
    existing_keys = {(r['pattern'], r['rule_type']) for r in existing}
    
    new_rows = [
        {
            "rule_id": f"pii-{rt[:3].lower()}-{pat.replace('.', '-')}",
            "rule_type": rt,
            "match_type": mt,
            "pattern": pat,
            "added_by": "pii_classifier",
            "notes": notes,
        }
        for rt, mt, pat, notes in GOVERNANCE_RULES
        if (pat, rt) not in existing_keys
    ]
    
    if new_rows:
        errors = client.insert_rows_json(table_ref, new_rows)
        if errors:
            print(f"  ⚠️  Insert errors: {errors}")
        else:
            print(f"  ✓ Inserted {len(new_rows)} governance rules")
    else:
        print(f"  ✓ All {len(GOVERNANCE_RULES)} rules already exist — nothing to add")

    print("\n📦 Step 2: Deploying Layer 1 procedure...")
    run_statement(LAYER1_PROC_SQL, "CREATE PROCEDURE layer1_domain_classify")

    print("\n📦 Step 3: Deploying Layer 2 procedure...")
    run_statement(LAYER2_PROC_SQL, "CREATE PROCEDURE layer2_ai_classify")

    print("\n📦 Step 4: Deploying views...")
    for name, sql in VIEWS_SQL.items():
        run_statement(sql, f"CREATE VIEW {name}")

    print("\n✅ Deployment complete.\n")



def run_layer1():
    """Layer 1: Domain-based classification — runs each UPDATE directly (avoids CALL timeout)."""
    print("\n\U0001f535 Running Layer 1 (domain blocklist)...")

    T = f"`{PROJECT_ID}.{DATASET_ID}.staging_raw_emails`"
    R = f"`{PROJECT_ID}.{DATASET_ID}.dim_governance_rules`"
    # BQ streaming buffer guard: DML cannot touch rows inserted in the last ~90 min.
    BG = "AND e.ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)"
    BG_S = "AND ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)"  # no alias needed

    updates = [
        ("PERSONAL (domain match)",
         f"UPDATE {T} e SET security_verdict = 'PERSONAL', processing_status = 'CLASSIFIED_L1' "
         f"WHERE e.processing_status = 'PENDING' {BG} AND EXISTS ("
         f"  SELECT 1 FROM {R} r WHERE r.rule_type = 'PERSONAL' AND ("
         f"    (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))"
         f"    OR (r.match_type = 'EXACT_EMAIL' AND LOWER(e.sender) = LOWER(r.pattern))))"),
        ("MARKETING (domain match)",
         f"UPDATE {T} e SET security_verdict = 'MARKETING', processing_status = 'CLASSIFIED_L1' "
         f"WHERE e.processing_status = 'PENDING' {BG} AND EXISTS ("
         f"  SELECT 1 FROM {R} r WHERE r.rule_type = 'MARKETING' AND ("
         f"    (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))"
         f"    OR (r.match_type = 'EXACT_EMAIL' AND LOWER(e.sender) = LOWER(r.pattern))))"),
        ("SYSTEM (domain match)",
         f"UPDATE {T} e SET security_verdict = 'SYSTEM', processing_status = 'CLASSIFIED_L1' "
         f"WHERE e.processing_status = 'PENDING' {BG} AND EXISTS ("
         f"  SELECT 1 FROM {R} r WHERE r.rule_type = 'SYSTEM' AND ("
         f"    (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))"
         f"    OR (r.match_type = 'EXACT_EMAIL' AND LOWER(e.sender) = LOWER(r.pattern))))"),
        ("BUSINESS (internal allow)",
         f"UPDATE {T} e SET security_verdict = 'BUSINESS', processing_status = 'CLASSIFIED_L1' "
         f"WHERE e.processing_status = 'PENDING' {BG} AND EXISTS ("
         f"  SELECT 1 FROM {R} r WHERE r.rule_type = 'ALLOW' AND ("
         f"    (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))"
         f"    OR (r.match_type = 'EXACT_EMAIL' AND LOWER(e.sender) = LOWER(r.pattern))))"),
        ("PERSONAL (subject pattern)",
         f"UPDATE {T} SET security_verdict = 'PERSONAL', ai_category = 'SUBJECT_PATTERN_MATCH', "
         f"processing_status = 'CLASSIFIED_L1' WHERE processing_status = 'PENDING' {BG_S} "
         f"AND REGEXP_CONTAINS(LOWER(subject), r'\\\\b(unsubscribe|newsletter|your order|shipment|delivery|tracking number|your account|password reset|verify your email|confirm your email|receipt|bank statement|statement of account|loan|insurance|medical aid|discovery health|momentum|liberty|old mutual|fnb|nedbank|absa|standard bank|capitec|nedgroup)\\\\b')"),
    ]

    for label, sql in updates:
        run_statement(sql, f"UPDATE \u2192 {label}")

    rows = run_query(
        f"SELECT security_verdict, COUNT(*) as n FROM {T} "
        f"WHERE processing_status = 'CLASSIFIED_L1' GROUP BY 1 ORDER BY n DESC",
        "L1 summary"
    )
    print("\n  Layer 1 results (cumulative):")
    for r in rows:
        print(f"    {str(r.get('security_verdict') or 'null'):<16} {r.get('n', 0):>10,}")
    print(f"  Remaining PENDING for Layer 2: {pending_count():,}")
    print("\u2705 Layer 1 complete.\n")


def run_layer2(batch_size: int, max_loops: int):
    """
    Layer 2: AI classifier on remaining PENDING emails.
    Uses BigQuery ML.GENERATE_TEXT (Gemini Flash) via scripting job.
    Cost: ~$0.03 per 1000-email batch. Full 360K corpus ≈ $11.
    """
    print(f"\n\U0001f7e3 Running Layer 2 (AI classifier) — up to {max_loops} batches of {batch_size}...")

    T = f"`{PROJECT_ID}.{DATASET_ID}.staging_raw_emails`"
    BG = "AND ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)"

    BATCH_SQL = f"""
    CREATE TEMP TABLE pending_ai AS
    SELECT message_id, sender, subject, snippet
    FROM {T}
    WHERE processing_status = 'PENDING' {BG}
    LIMIT {batch_size};

    CREATE TEMP TABLE ai_results AS
    SELECT message_id, ml_generate_text_llm_result AS raw
    FROM ML.GENERATE_TEXT(
      MODEL `{PROJECT_ID}.{DATASET_ID}.gemini_flash`,
      (SELECT message_id,
        CONCAT(
          'Privacy classifier for corporate email. ONE category only. JSON only, no markdown.\\n',
          'Categories: BUSINESS|PERSONAL|HR_SENSITIVE|CONFIDENTIAL|MARKETING|SYSTEM\\n',
          'BUSINESS=work/client/ops, PERSONAL=private life/family/finances/health,\\n',
          'HR_SENSITIVE=salary/HR/medical, CONFIDENTIAL=legal/board/NDA,\\n',
          'MARKETING=newsletter/promo(unsolicited), SYSTEM=automated/alert/notification\\n',
          'From:', sender, ' Subject:', subject, ' Preview:', snippet, '\\n',
          'JSON: {{"verdict":"CATEGORY","confidence":0.9,"reason":"brief"}}'
        ) AS prompt
      FROM pending_ai),
      STRUCT(0.1 AS temperature, 120 AS max_output_tokens, TRUE AS flatten_json_output));

    UPDATE {T} e
    SET security_verdict = JSON_VALUE(r.raw, '$.verdict'),
        ai_category = CONCAT('AI_L2:', COALESCE(JSON_VALUE(r.raw, '$.reason'), 'ok')),
        processing_status = 'CLASSIFIED_L2'
    FROM ai_results r
    WHERE e.message_id = r.message_id
      AND JSON_VALUE(r.raw, '$.verdict') IS NOT NULL;

    UPDATE {T} e
    SET security_verdict = 'BUSINESS', ai_category = 'AI_L2_PARSE_FAIL', processing_status = 'CLASSIFIED_L2'
    FROM ai_results r
    WHERE e.message_id = r.message_id
      AND JSON_VALUE(r.raw, '$.verdict') IS NULL;
    """

    total_processed = 0
    for i in range(max_loops):
        remaining = pending_count()
        if remaining == 0:
            print(f"\n  \U0001f389 All emails classified after {i} batches!")
            break

        print(f"\n  Batch {i+1}/{max_loops} — {remaining:,} remaining", end="", flush=True)

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("batch_size", "INT64", batch_size)
            ]
        )
        job = client.query(BATCH_SQL, job_config=job_config, location="US")

        waited = 0
        while not job.done():
            time.sleep(5)
            waited += 5
            print(".", end="", flush=True)
            if waited > 900:  # 15 min per batch max
                print(f" TIMEOUT")
                break
        print(f" ({waited}s)")

        try:
            job.result()
        except Exception as e:
            print(f"  \u26a0\ufe0f  Batch error: {e}")
            time.sleep(10)
            continue

        total_processed += batch_size
        time.sleep(3)  # brief pause between batches

    # Final summary
    rows = run_query(
        f"SELECT security_verdict, COUNT(*) as n FROM {T} "
        f"WHERE processing_status = 'CLASSIFIED_L2' GROUP BY 1 ORDER BY n DESC",
        "L2 summary"
    )
    print("\n  Layer 2 results (classified this session):")
    for r in rows:
        print(f"    {str(r.get('security_verdict') or 'null'):<16} {r.get('n', 0):>10,}")
    print(f"\n\u2705 Layer 2 done. ~{total_processed:,} emails processed.\n")


def show_summary():
    """Print the classification breakdown."""
    print("\n📊 Classification Summary:\n")
    rows = run_query(
        f"SELECT security_verdict, email_count, pct_of_total, distinct_sender_domains "
        f"FROM `{PROJECT_ID}.{DATASET_ID}.v_classification_summary` "
        f"ORDER BY email_count DESC",
        "Fetching summary"
    )
    if not rows:
        print("  No data yet. Run --layer1 first.")
        return

    print(f"  {'VERDICT':<20} {'COUNT':>10} {'%':>6} {'DOMAINS':>10}")
    print(f"  {'-'*20} {'-'*10} {'-'*6} {'-'*10}")
    for r in rows:
        verdict  = str(r.get("security_verdict") or "UNCLASSIFIED")
        count    = r.get("email_count", 0)
        pct      = r.get("pct_of_total", 0)
        domains  = r.get("distinct_sender_domains", 0)
        print(f"  {verdict:<20} {count:>10,} {pct:>5.1f}% {domains:>10,}")
    print()


def personal_audit(limit: int = 50):
    """Show subject lines of flagged personal/sensitive emails for review."""
    print(f"\n🔍 Personal/Sensitive Email Sample (top {limit}):\n")
    rows = run_query(
        f"""
        SELECT security_verdict, sender, subject, ai_category, timestamp
        FROM `{PROJECT_ID}.{DATASET_ID}.v_personal_flagged`
        ORDER BY timestamp DESC
        LIMIT {limit}
        """,
        "Fetching personal flagged sample"
    )
    if not rows:
        print("  None flagged yet. Run classification first.\n")
        return

    for r in rows:
        verdict = r.get("security_verdict", "?")
        sender  = (r.get("sender") or "?")[:35]
        subject = (r.get("subject") or "(no subject)")[:60]
        print(f"  [{verdict:<12}] {sender:<35} | {subject}")
    print()


def show_business_count():
    """How many clean business emails are ready for agents/KB."""
    rows = run_query(
        f"SELECT COUNT(*) as n FROM `{PROJECT_ID}.{DATASET_ID}.v_business_emails`",
        "Business email count"
    )
    count = rows[0]["n"] if rows else 0
    print(f"\n✅ Clean business emails available for KB/agents: {count:,}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="HiveMind Personal Email Classifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--deploy",        action="store_true", help="Deploy SQL procedures and views")
    parser.add_argument("--layer1",        action="store_true", help="Run Layer 1 domain classifier")
    parser.add_argument("--layer2",        action="store_true", help="Run Layer 2 AI classifier")
    parser.add_argument("--batch",  type=int, default=500,       help="Batch size for Layer 2 (default: 500)")
    parser.add_argument("--loops",  type=int, default=10,        help="Max batches for Layer 2 (default: 10)")
    parser.add_argument("--summary",       action="store_true", help="Show classification summary")
    parser.add_argument("--personal-audit",action="store_true", help="Show sample of flagged personal emails")
    parser.add_argument("--business-count",action="store_true", help="Count of clean business emails ready for use")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(0)

    if args.deploy:
        deploy()
    if args.layer1:
        run_layer1()
    if args.layer2:
        run_layer2(args.batch, args.loops)
    if args.summary:
        show_summary()
    if args.personal_audit:
        personal_audit()
    if args.business_count:
        show_business_count()


if __name__ == "__main__":
    main()
