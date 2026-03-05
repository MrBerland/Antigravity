"""
activate_watch_all_users.py
============================
Registers Gmail push notifications (users.watch) for ALL monitored mailboxes
using the service account with Domain-Wide Delegation.

The original activate_watch.sh only watches 'me' (Tim's ADC credentials).
This script impersonates each user and registers the watch for all of them.

Gmail watch() expires every 7 days — run this script weekly, or automate
it with Cloud Scheduler calling this via Cloud Run / Cloud Functions.

Usage:
    python3 /Users/timstevens/Antigravity/HiveMind/activate_watch_all_users.py
"""

import os
import json
import sys
from datetime import datetime, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ── Config ────────────────────────────────────────────────────────────────────
_SCRIPT_DIR     = os.path.dirname(os.path.abspath(__file__))
SA_FILE         = os.path.join(_SCRIPT_DIR, "credentials", "hive-mind-admin.json")
USERS_FILE      = os.path.join(_SCRIPT_DIR, "config", "users_list.json")
PROJECT_ID      = "augos-core-data"
TOPIC_NAME      = f"projects/{PROJECT_ID}/topics/gmail-ingest-topic"
SCOPES          = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]

# ── Load users ────────────────────────────────────────────────────────────────
with open(USERS_FILE) as f:
    ALL_USERS = json.load(f)

# Skip obvious non-person mailboxes that don't need watching
SKIP_USERS = {"canned.response@augos.io", "tim+canned.response@augos.io", "notifications@augos.io"}

WATCH_USERS = [u for u in ALL_USERS if u not in SKIP_USERS]

print(f"\n📡 Gmail Watch Renewal — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
print(f"   Project:   {PROJECT_ID}")
print(f"   Topic:     {TOPIC_NAME}")
print(f"   Users:     {len(WATCH_USERS)}\n")


def get_gmail_service(user_email: str):
    creds = service_account.Credentials.from_service_account_file(SA_FILE, scopes=SCOPES)
    creds = creds.with_subject(user_email)
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


results = {"success": [], "failed": [], "skipped": []}

for user in WATCH_USERS:
    try:
        service = get_gmail_service(user)
        response = service.users().watch(
            userId="me",
            body={
                "labelIds": ["INBOX"],
                "topicName": TOPIC_NAME,
                "labelFilterAction": "include",
            }
        ).execute()

        expiry_ms  = int(response.get("expiration", 0))
        expiry_dt  = datetime.fromtimestamp(expiry_ms / 1000, tz=timezone.utc)
        history_id = response.get("historyId", "?")

        print(f"  ✅ {user:<38} historyId={history_id}  expires={expiry_dt.strftime('%Y-%m-%d %H:%M UTC')}")
        results["success"].append(user)

    except HttpError as e:
        status = e.resp.status
        reason = e.reason if hasattr(e, "reason") else str(e)
        print(f"  ❌ {user:<38} HTTP {status}: {reason}")
        results["failed"].append((user, f"HTTP {status}: {reason}"))
    except Exception as e:
        print(f"  ⚠️  {user:<38} Error: {e}")
        results["failed"].append((user, str(e)))


print(f"\n{'─'*60}")
print(f"  ✅ Watching:  {len(results['success'])} mailboxes")
print(f"  ❌ Failed:    {len(results['failed'])} mailboxes")

if results["failed"]:
    print("\n  Failed mailboxes:")
    for user, reason in results["failed"]:
        print(f"    • {user}: {reason}")

print(f"\n⚠️  Watches expire in 7 days. Re-run this script before then.\n")
print(f"   Automate: add a weekly Cloud Scheduler job targeting this script.")
