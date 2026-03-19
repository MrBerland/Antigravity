"""
Email Reader — Gmail API via Service Account
============================================
Reads emails from tim@augos.io inbox using service account with domain-wide
delegation. Requires gmail.readonly scope in Workspace Admin delegation.

Uses:
  - Read recent report emails to assess quality
  - Pull inbox for analysis and context
  - Find specific email threads by subject or sender
"""

import base64
import email
import logging
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

_SCOPES_READ = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]
_PROJECT_ROOT = Path(__file__).parent.parent.parent


def _build_gmail_read_service():
    """Build Gmail API service with send+read scopes."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    sa_path = os.getenv("GMAIL_SERVICE_ACCOUNT_PATH", "credentials/service_account.json")
    sa_file = _PROJECT_ROOT / sa_path
    if not sa_file.exists():
        raise FileNotFoundError(f"Service account JSON not found at: {sa_file}")

    delegate = os.getenv("GMAIL_DELEGATE_ADDRESS", "")
    if not delegate:
        raise ValueError("GMAIL_DELEGATE_ADDRESS not set in .env")

    creds = service_account.Credentials.from_service_account_file(
        str(sa_file), scopes=_SCOPES_READ
    ).with_subject(delegate)

    return build("gmail", "v1", credentials=creds)


def _decode_body(payload: dict) -> str:
    """Extract plain text or HTML body from Gmail message payload."""
    text = ""
    if "parts" in payload:
        for part in payload["parts"]:
            mime = part.get("mimeType", "")
            data = part.get("body", {}).get("data", "")
            if mime == "text/plain" and data:
                text = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="ignore")
                break
            elif mime == "text/html" and data and not text:
                raw = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="ignore")
                # Strip HTML tags for readable plain text
                text = re.sub(r"<[^>]+>", " ", raw)
                text = re.sub(r"\s+", " ", text).strip()
    else:
        data = payload.get("body", {}).get("data", "")
        if data:
            text = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="ignore")
    return text.strip()


def _parse_headers(headers: list) -> dict:
    """Parse message headers into a dict."""
    return {h["name"].lower(): h["value"] for h in headers}


def get_recent_report_emails(days_back: int = 3, max_results: int = 20) -> List[Dict[str, Any]]:
    """
    Fetch recent Utility Intelligence Manager report emails.

    Args:
        days_back: How many days back to search (default 3)
        max_results: Maximum number of emails to return

    Returns:
        List of email dicts with subject, date, body_text, persona, findings_summary
    """
    service = _build_gmail_read_service()
    delegate = os.getenv("GMAIL_DELEGATE_ADDRESS", "")

    # Build query
    after_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y/%m/%d")
    query = f'from:{delegate} ("Utility Manager" OR "Utility Brief" OR "Chief Engineer" OR "General Manager") after:{after_date}'

    result = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()

    messages = result.get("messages", [])
    if not messages:
        return []

    emails = []
    for msg_ref in messages:
        msg = service.users().messages().get(
            userId="me", id=msg_ref["id"], format="full"
        ).execute()

        headers = _parse_headers(msg["payload"].get("headers", []))
        subject = headers.get("subject", "")
        date_str = headers.get("date", "")
        body = _decode_body(msg["payload"])

        # Infer persona from subject
        persona = "unknown"
        if "Chief Engineer" in subject:
            persona = "chief_engineer"
        elif "General Manager" in subject:
            persona = "general_manager"
        elif "Sustainability" in subject:
            persona = "sustainability_officer"
        elif "Financial" in subject:
            persona = "financial_controller"

        # Extract finding counts from subject
        critical = re.search(r"(\d+) Critical", subject)
        warnings = re.search(r"(\d+) Warning", subject)

        emails.append({
            "message_id": msg_ref["id"],
            "subject": subject,
            "date": date_str,
            "persona": persona,
            "all_clear": "All Clear" in subject,
            "critical_count": int(critical.group(1)) if critical else 0,
            "warning_count": int(warnings.group(1)) if warnings else 0,
            "body_text": body[:3000],  # Trim to 3000 chars for readability
        })

    return emails


def get_email_by_subject(subject_contains: str, days_back: int = 7) -> Optional[Dict[str, Any]]:
    """
    Find a specific email by subject text.

    Args:
        subject_contains: Partial subject string to search for
        days_back: How many days back to search

    Returns:
        Email dict or None if not found
    """
    service = _build_gmail_read_service()
    after_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y/%m/%d")
    query = f'subject:"{subject_contains}" after:{after_date}'

    result = service.users().messages().list(userId="me", q=query, maxResults=5).execute()
    messages = result.get("messages", [])
    if not messages:
        return None

    msg = service.users().messages().get(
        userId="me", id=messages[0]["id"], format="full"
    ).execute()
    headers = _parse_headers(msg["payload"].get("headers", []))

    return {
        "message_id": messages[0]["id"],
        "subject": headers.get("subject", ""),
        "date": headers.get("date", ""),
        "body_text": _decode_body(msg["payload"]),
    }


def assess_recent_reports() -> Dict[str, Any]:
    """
    Pull and assess all recent Utility Manager report emails.

    Returns a structured summary of what reports have been sent,
    what they found, and any quality issues.
    """
    emails = get_recent_report_emails(days_back=3)
    if not emails:
        return {"status": "no_reports", "message": "No report emails found in the last 3 days."}

    summary = {
        "status":         "ok",
        "reports_found":  len(emails),
        "personas":       {},
        "total_critical": 0,
        "total_warnings": 0,
        "all_clear_count": 0,
    }

    for e in emails:
        p = e["persona"]
        summary["personas"][p] = {
            "subject":      e["subject"],
            "date":         e["date"],
            "all_clear":    e["all_clear"],
            "critical":     e["critical_count"],
            "warnings":     e["warning_count"],
        }
        summary["total_critical"] += e["critical_count"]
        summary["total_warnings"] += e["warning_count"]
        if e["all_clear"]:
            summary["all_clear_count"] += 1

    return summary
