#!/bin/bash

# Ensure GCloud is in PATH
export PATH=$PATH:$HOME/google-cloud-sdk/bin

# Check Auth
if ! gcloud auth print-access-token >/dev/null 2>&1; then
    echo "❌ Error: You are not logged in to gcloud."
    echo "Please run: 'gcloud auth login' and try again."
    exit 1
fi

# Configuration

# Configuration
PROJECT_ID="augos-core-data"
REGION="us-central1"
BUCKET_NAME="${PROJECT_ID}-raw-email-lake"

echo "🚀 Starting Hive Mind Deployment via GCloud..."
echo "Target Project: $PROJECT_ID"

# 1. Enable APIs (Best Effort)
echo "--- Step 1: Enabling APIs ---"
gcloud services enable gmail.googleapis.com pubsub.googleapis.com cloudfunctions.googleapis.com bigquery.googleapis.com artifactregistry.googleapis.com run.googleapis.com --project=$PROJECT_ID

# 2. Pub/Sub
echo "--- Step 2: Creating Pub/Sub Topic ---"
gcloud pubsub topics create gmail-ingest-topic --project=$PROJECT_ID || echo "Topic likely exists."

# 3. GCS Bucket
echo "--- Step 3: Creating GCS Bucket ---"
gsutil mb -p $PROJECT_ID -l US gs://$BUCKET_NAME || echo "Bucket likely exists."

# 4. BigQuery
echo "--- Step 4: Creating BigQuery Dataset & Table ---"
bq --project_id=$PROJECT_ID mk -d --location=US hive_mind_core || echo "Dataset exists."
bq --project_id=$PROJECT_ID mk --table hive_mind_core.messages ./HiveMind/infrastructure/bq_schema_messages.json || echo "Table exists."

# 5. Cloud Function
echo "--- Step 5: Deploying Cloud Function (The Extractor) ---"
echo "Deploying from source: ./HiveMind/src/extractor"

gcloud functions deploy hive-mind-extractor \
    --project=$PROJECT_ID \
    --region=$REGION \
    --runtime=python310 \
    --trigger-topic=gmail-ingest-topic \
    --source=./HiveMind/src/extractor \
    --entry-point=ingest_gmail_event \
    --set-env-vars=PROJECT_ID=$PROJECT_ID,BUCKET_NAME=$BUCKET_NAME,DATASET_ID=hive_mind_core,TABLE_ID=messages \
    --allow-unauthenticated

echo "✅ Deployment Script Finished."
