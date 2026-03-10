#!/bin/bash
# deploy_gcloud.sh
# ================
# Full HiveMind GCP deployment script.
# Run from project root: bash HiveMind/deploy_gcloud.sh

set -e

export PATH=$PATH:$HOME/google-cloud-sdk/bin

# ── Auth check ────────────────────────────────────────────────────────────────
if ! gcloud auth print-access-token > /dev/null 2>&1; then
    echo "❌ Not logged in. Run: gcloud auth login"
    exit 1
fi

# ── Configuration ─────────────────────────────────────────────────────────────
PROJECT_ID="augos-core-data"
REGION="us-central1"
BUCKET_NAME="${PROJECT_ID}-raw-email-lake"
DATASET="hive_mind_core"
SA_EMAIL="hive-mind-admin@${PROJECT_ID}.iam.gserviceaccount.com"

# Load monitored users from config (JSON array)
USERS_FILE="HiveMind/config/users_list.json"
WATCH_USERS=$(cat "$USERS_FILE" | tr -d '\n ')

echo "🚀 HiveMind Deployment — project: $PROJECT_ID"
echo ""

# ── Step 1: Enable APIs ───────────────────────────────────────────────────────
echo "--- Step 1: Enabling APIs ---"
gcloud services enable \
    gmail.googleapis.com \
    pubsub.googleapis.com \
    cloudfunctions.googleapis.com \
    cloudscheduler.googleapis.com \
    bigquery.googleapis.com \
    bigquerymigration.googleapis.com \
    aiplatform.googleapis.com \
    artifactregistry.googleapis.com \
    run.googleapis.com \
    --project=$PROJECT_ID

# ── Step 2: Pub/Sub ───────────────────────────────────────────────────────────
echo "--- Step 2: Pub/Sub Topic ---"
gcloud pubsub topics create gmail-ingest-topic --project=$PROJECT_ID 2>/dev/null || echo "  Topic exists."

# ── Step 3: GCS Bucket ───────────────────────────────────────────────────────
echo "--- Step 3: GCS Bucket ---"
gsutil mb -p $PROJECT_ID -l US gs://$BUCKET_NAME 2>/dev/null || echo "  Bucket exists."

# ── Step 4: BigQuery datasets and core tables ─────────────────────────────────
echo "--- Step 4: BigQuery ---"
bq --project_id=$PROJECT_ID mk -d --location=US $DATASET 2>/dev/null || echo "  Dataset exists."
bq --project_id=$PROJECT_ID mk --table ${DATASET}.staging_raw_emails \
    ./HiveMind/infrastructure/bq_schema_messages.json 2>/dev/null || echo "  Staging table exists."

# Watermarks table (idempotent)
bq --project_id=$PROJECT_ID query --use_legacy_sql=false \
    "$(cat HiveMind/src/sql/create_watermarks_table.sql)" 2>/dev/null || echo "  Watermarks table exists."

# Agent output tables (idempotent)
bq --project_id=$PROJECT_ID query --use_legacy_sql=false \
    "$(cat HiveMind/src/sql/create_agent_tables.sql)" 2>/dev/null || echo "  Agent tables seeded."
bq --project_id=$PROJECT_ID query --use_legacy_sql=false \
    "$(cat HiveMind/src/sql/create_workforce_tables.sql)" 2>/dev/null || echo "  Workforce tables seeded."
bq --project_id=$PROJECT_ID query --use_legacy_sql=false \
    "$(cat HiveMind/src/sql/create_entity_tables.sql)" 2>/dev/null || echo "  Entity tables seeded."
bq --project_id=$PROJECT_ID query --use_legacy_sql=false \
    "$(cat HiveMind/src/sql/create_governance_tables.sql)" 2>/dev/null || echo "  Governance tables seeded."

# ── Step 5: Deploy Gemini BQML model ─────────────────────────────────────────
echo "--- Step 5: BQML Models ---"
bq --project_id=$PROJECT_ID query --use_legacy_sql=false \
    "$(cat HiveMind/src/sql/create_gemini_model.sql)" 2>/dev/null || echo "  Gemini model exists."

# ── Step 6: Deploy Ops View ───────────────────────────────────────────────────
echo "--- Step 6: Ops View ---"
bq --project_id=$PROJECT_ID query --use_legacy_sql=false \
    "$(cat HiveMind/src/sql/create_ops_view.sql)" 2>/dev/null || echo "  Ops view deployed."

# ── Step 7: Deploy Cloud Function (Extractor — Pub/Sub trigger) ──────────────
echo "--- Step 7: Cloud Function — hive-mind-extractor ---"
gcloud functions deploy hive-mind-extractor \
    --project=$PROJECT_ID \
    --region=$REGION \
    --runtime=python311 \
    --trigger-topic=gmail-ingest-topic \
    --source=./HiveMind/src/extractor \
    --entry-point=ingest_gmail_event \
    --service-account=$SA_EMAIL \
    --set-env-vars="PROJECT_ID=${PROJECT_ID},BUCKET_NAME=${BUCKET_NAME},DATASET_ID=${DATASET},TABLE_ID=staging_raw_emails" \
    --memory=512MB \
    --timeout=120s \
    --no-allow-unauthenticated

# ── Step 8: Deploy Cloud Function (Watch Renewal — HTTP trigger) ──────────────
echo "--- Step 8: Cloud Function — hive-mind-watch-renewal ---"
gcloud functions deploy hive-mind-watch-renewal \
    --project=$PROJECT_ID \
    --region=$REGION \
    --runtime=python311 \
    --trigger-http \
    --source=./HiveMind/src/extractor \
    --entry-point=renew_gmail_watches \
    --service-account=$SA_EMAIL \
    --set-env-vars="PROJECT_ID=${PROJECT_ID},DATASET_ID=${DATASET},WATCH_USERS=${WATCH_USERS}" \
    --memory=256MB \
    --timeout=120s \
    --no-allow-unauthenticated

WATCH_URL=$(gcloud functions describe hive-mind-watch-renewal \
    --project=$PROJECT_ID --region=$REGION \
    --format='value(serviceConfig.uri)' 2>/dev/null || echo "")

# ── Step 9: Cloud Scheduler — weekly Gmail Watch renewal ─────────────────────
echo "--- Step 9: Cloud Scheduler ---"
if gcloud scheduler jobs describe hive-mind-watch-renewal \
    --project=$PROJECT_ID --location=$REGION > /dev/null 2>&1; then
    echo "  Scheduler job exists — updating..."
    SCHED_CMD="update"
else
    SCHED_CMD="create"
fi

gcloud scheduler jobs $SCHED_CMD http hive-mind-watch-renewal \
    --project=$PROJECT_ID \
    --location=$REGION \
    --schedule="0 6 * * 1" \
    --uri="${WATCH_URL}" \
    --http-method=POST \
    --oidc-service-account-email=$SA_EMAIL \
    --description="Weekly Gmail Watch renewal for HiveMind (every Monday 06:00 UTC)" \
    2>/dev/null || echo "  Scheduler job created/updated."

# ── Step 10: Initial Gmail Watch activation ───────────────────────────────────
echo "--- Step 10: Activating Gmail Watch for all users ---"
python3 HiveMind/activate_watch_all_users.py

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "  1. Run the classifier:    python3 HiveMind/src/sql/run_classifier.py --layer1 --layer2 --batch 1000 --loops 500"
echo "  2. Run agent pipeline:    nohup python3 HiveMind/hivemind_pipeline.py > /tmp/hivemind_pipeline.log 2>&1 &"
echo "  3. Start UI:              cd hive-mind-ui && npm run dev"
echo "  4. Watch renewal auto-runs every Monday 06:00 UTC via Cloud Scheduler."
