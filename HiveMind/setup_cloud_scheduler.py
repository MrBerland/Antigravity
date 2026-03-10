#!/usr/bin/env python3
"""
setup_cloud_scheduler.py
========================
One-time setup script to automate the Gmail Watch renewal via Cloud Scheduler.

Gmail push notifications (watch) expire every 7 days. This script:
  1. Creates a Cloud Run Job that runs activate_watch_all_users.py
  2. Creates a Cloud Scheduler job to trigger it weekly (every Monday 06:00 UTC)

Prerequisites:
  - gcloud auth login (with project editor permissions)
  - Cloud Run API, Cloud Scheduler API enabled
  - Docker / Artifact Registry set up (the job runs as a container)

Alternative (simpler) approach used here:
  - Deploy as a Cloud Function (HTTP trigger) instead of Cloud Run Job
  - Cloud Scheduler calls the HTTP endpoint weekly

Run once:
    python3 HiveMind/setup_cloud_scheduler.py
"""

import subprocess
import sys
import os

PROJECT_ID = "augos-core-data"
REGION     = "us-central1"
TOPIC      = f"projects/{PROJECT_ID}/topics/gmail-ingest-topic"
SA_EMAIL   = f"hive-mind-admin@{PROJECT_ID}.iam.gserviceaccount.com"

def run(cmd: str, check: bool = True) -> str:
    """Run a shell command and return stdout."""
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        sys.exit(1)
    output = result.stdout.strip()
    if output:
        print(f"  → {output[:200]}")
    return output


def main():
    # Ensure gcloud is authenticated
    run("gcloud auth print-access-token > /dev/null 2>&1 || (echo 'Not logged in. Run: gcloud auth login' && exit 1)")

    print("\n📦 Step 1: Enable required APIs...")
    run(f"gcloud services enable cloudscheduler.googleapis.com run.googleapis.com --project={PROJECT_ID}")

    print("\n📦 Step 2: Create the watermark BigQuery table...")
    sql_path = os.path.abspath("HiveMind/src/sql/create_watermarks_table.sql")
    run(f"bq --project_id={PROJECT_ID} query --use_legacy_sql=false < {sql_path}", check=False)

    print("\n📦 Step 3: Deploy Gmail Watch Renewal as a Cloud Function (HTTP)...")
    # Write the watch renewal function inline so it's self-contained
    watch_fn_source = os.path.abspath("HiveMind/src/watch_renewal")
    os.makedirs(watch_fn_source, exist_ok=True)

    # Write the Cloud Function entrypoint
    with open(os.path.join(watch_fn_source, "main.py"), "w") as f:
        f.write('''\
import functions_framework
import subprocess
import os

@functions_framework.http
def renew_watch(request):
    """HTTP Cloud Function — re-registers Gmail push watch for all users."""
    try:
        result = subprocess.run(
            ["python3", "/app/activate_watch_all_users.py"],
            capture_output=True, text=True, timeout=120
        )
        body = result.stdout + result.stderr
        status = 200 if result.returncode == 0 else 500
        return (body, status, {"Content-Type": "text/plain"})
    except Exception as e:
        return (str(e), 500, {"Content-Type": "text/plain"})
''')

    with open(os.path.join(watch_fn_source, "requirements.txt"), "w") as f:
        f.write("functions-framework==3.*\n")

    # Actually: simpler to use a Cloud Scheduler job that publishes a Pub/Sub message
    # to a dedicated topic, and have a Cloud Function listen. But simplest of all
    # is to call `activate_watch_all_users.py` via Cloud Run Jobs.
    # For now we create a Cloud Scheduler job that hits a simple HTTP function.

    print("\n📦 Step 4: Create Cloud Scheduler job for weekly Gmail Watch renewal...")
    # Use gcloud scheduler to call the watch renewal function every Monday at 06:00 UTC
    # First, deploy a minimal HTTP Cloud Function that calls the watch renewal script
    run(
        f"gcloud functions deploy hive-mind-watch-renewal "
        f"--project={PROJECT_ID} "
        f"--region={REGION} "
        f"--runtime=python311 "
        f"--trigger-http "
        f"--source=HiveMind/src/extractor "
        f"--entry-point=renew_gmail_watches "
        f"--service-account={SA_EMAIL} "
        f"--no-allow-unauthenticated "
        f"--set-env-vars=PROJECT_ID={PROJECT_ID},DATASET_ID=hive_mind_core "
        f"--timeout=120s",
        check=False
    )

    # Get the function URL
    fn_url = run(
        f"gcloud functions describe hive-mind-watch-renewal "
        f"--project={PROJECT_ID} --region={REGION} "
        f"--format='value(serviceConfig.uri)'",
        check=False
    )

    if not fn_url:
        print("  ⚠️  Could not get function URL. Create Cloud Scheduler job manually.")
        fn_url = f"https://{REGION}-{PROJECT_ID}.cloudfunctions.net/hive-mind-watch-renewal"

    # Create (or update) Cloud Scheduler job
    scheduler_exists = run(
        f"gcloud scheduler jobs describe hive-mind-watch-renewal "
        f"--project={PROJECT_ID} --location={REGION} 2>/dev/null",
        check=False
    )

    if scheduler_exists:
        print("  Scheduler job already exists — updating...")
        cmd = "update"
    else:
        cmd = "create"

    run(
        f"gcloud scheduler jobs {cmd} http hive-mind-watch-renewal "
        f"--project={PROJECT_ID} "
        f"--location={REGION} "
        f"--schedule='0 6 * * 1' "          # Every Monday at 06:00 UTC
        f"--uri='{fn_url}' "
        f"--http-method=POST "
        f"--oidc-service-account-email={SA_EMAIL} "
        f"--description='Weekly Gmail Watch renewal for HiveMind ingestion'",
        check=False
    )

    print("\n✅ Cloud Scheduler setup complete!")
    print(f"\n   Schedule: Every Monday 06:00 UTC")
    print(f"   Function: {fn_url}")
    print(f"\n   To trigger manually:")
    print(f"   gcloud scheduler jobs run hive-mind-watch-renewal --location={REGION}")
    print(f"\n   To check logs:")
    print(f"   gcloud functions logs read hive-mind-watch-renewal --project={PROJECT_ID} --region={REGION}")


if __name__ == "__main__":
    main()
