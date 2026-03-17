"""
Email Sender — Gmail API via Service Account
============================================
Sends persona-specific utility intelligence reports via Gmail API.
Uses service account with domain-wide delegation.

No passwords stored. No manual rotation. Fully autonomous.

Prerequisites (one-time setup):
  See: knowledge/SETUP_GMAIL_API.md

Environment variables required:
  GMAIL_SERVICE_ACCOUNT_PATH=credentials/service_account.json
  GMAIL_DELEGATE_ADDRESS=sender@yourdomain.com
  CHIEF_ENGINEER_EMAIL, GM_EMAIL, FINANCE_EMAIL, SUSTAINABILITY_EMAIL
  EMAIL_FROM_NAME=Utility Intelligence Manager | One & Only Cape Town
"""

import base64
import logging
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_APPROVED_DOMAINS = {"augos.io"}  # Expanded only with explicit authorisation


# ─── Dev Mode Routing ───────────────────────────────────────────────────────────

def _is_dev_mode() -> bool:
    return os.getenv("DEV_MODE", "true").strip().lower() in ("true", "1", "yes")


def _dev_email() -> str:
    addr = os.getenv("DEV_EMAIL", "").strip()
    if not addr:
        raise ValueError(
            "DEV_EMAIL must be set in .env during development. "
            "Example: DEV_EMAIL=tim@augos.io"
        )
    return addr


def _resolve_recipient(intended_recipient: str, persona: str) -> tuple[str, bool]:
    """
    Resolve the actual delivery address.

    In DEV_MODE (default): all email goes to DEV_EMAIL regardless of intended recipient.
    In PROD_MODE: validates the intended recipient's domain against the approved list.

    Returns:
        (actual_recipient, is_intercepted)
    """
    if _is_dev_mode():
        return _dev_email(), True

    # Production: enforce domain allowlist
    domain = intended_recipient.split("@")[-1].lower() if "@" in intended_recipient else ""
    if domain not in _approved_domains():
        raise PermissionError(
            f"Recipient domain '{domain}' is not on the approved list. "
            f"Approved domains: {_approved_domains()}. "
            "Add domains explicitly via APPROVED_EMAIL_DOMAINS in .env."
        )
    return intended_recipient, False


def _approved_domains() -> set:
    """Return the set of approved recipient domains."""
    extra = os.getenv("APPROVED_EMAIL_DOMAINS", "")
    extras = {d.strip().lower() for d in extra.split(",") if d.strip()}
    return _APPROVED_DOMAINS | extras


def _dev_banner(intended_recipient: str, persona: str) -> str:
    """HTML banner shown on emails intercepted by dev mode."""
    return f"""
<div style="background:#451A03;border:1px solid #F59E0B;border-radius:8px;
  padding:12px 16px;margin-bottom:24px;">
  <div style="color:#FCD34D;font-size:12px;font-weight:700;letter-spacing:1px;
    text-transform:uppercase;margin-bottom:4px;">⚠️ Dev Mode — Email Intercepted</div>
  <div style="color:#FDE68A;font-size:13px;">
    Intended for: <strong>{intended_recipient}</strong>
    &nbsp;&middot;&nbsp; Persona: <strong>{persona.replace('_', ' ').title()}</strong>
  </div>
  <div style="color:#92400E;font-size:11px;margin-top:6px;">
    Set DEV_MODE=false in .env to enable live delivery. Only augos.io recipients permitted.
  </div>
</div>"""


def _build_gmail_service():
    """Build an authenticated Gmail API service using service account credentials."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        raise ImportError(
            "Gmail API libraries not installed. Run: "
            "pip install google-auth google-auth-httplib2 google-api-python-client"
        )

    creds_path = os.getenv("GMAIL_SERVICE_ACCOUNT_PATH", "credentials/service_account.json")
    full_path = _PROJECT_ROOT / creds_path

    if not full_path.exists():
        raise FileNotFoundError(
            f"Service account JSON not found at: {full_path}\n"
            "Follow the setup guide: knowledge/SETUP_GMAIL_API.md"
        )

    delegate = os.getenv("GMAIL_DELEGATE_ADDRESS", "").strip()
    if not delegate:
        raise ValueError("GMAIL_DELEGATE_ADDRESS must be set in .env")

    credentials = service_account.Credentials.from_service_account_file(
        str(full_path),
        scopes=_SCOPES,
    )
    delegated = credentials.with_subject(delegate)
    return build("gmail", "v1", credentials=delegated)


def _send_raw_email(service, to: str, subject: str, html_body: str, text_body: str) -> Dict:
    """Send an email via Gmail API. Returns the message resource."""
    from_name = os.getenv("EMAIL_FROM_NAME", "Utility Intelligence Manager")
    delegate = os.getenv("GMAIL_DELEGATE_ADDRESS", "")

    msg = MIMEMultipart("alternative")
    msg["to"] = to
    msg["from"] = f"{from_name} <{delegate}>"
    msg["subject"] = subject

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    log.info("Email sent to %s (id: %s)", to, result.get("id"))
    return result


# ─── HTML Email Templates ─────────────────────────────────────────────────────

_SEVERITY_COLOURS = {
    "P1_CRITICAL": "#EF4444",
    "P2_WARNING":  "#F59E0B",
    "P3_INSIGHT":  "#3B82F6",
    "P3_POSITIVE": "#10B981",
    "normal":      "#6B7280",
}

_SEVERITY_ICONS = {
    "P1_CRITICAL": "🔴",
    "P2_WARNING":  "⚠️",
    "P3_INSIGHT":  "💡",
    "P3_POSITIVE": "✅",
    "normal":      "ℹ️",
}


def _html_wrapper(content: str, title: str, subtitle: str,
                  dev_banner: str = "") -> str:
    """Wrap content in a professional hotel-branded HTML email template."""
    year = datetime.utcnow().year
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title></head>
<body style="margin:0;padding:0;background:#0F172A;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0F172A;padding:32px 0;">
<tr><td align="center">
<table width="620" cellpadding="0" cellspacing="0" style="max-width:620px;width:100%;">

<!-- HEADER -->
<tr><td style="background:linear-gradient(135deg,#1E293B 0%,#0F172A 100%);
  border-radius:12px 12px 0 0;padding:32px 40px;border-bottom:1px solid #1E3A5F;">
  <table width="100%"><tr>
    <td>
      <div style="color:#94A3B8;font-size:11px;letter-spacing:2px;text-transform:uppercase;
        font-weight:600;margin-bottom:4px;">One &amp; Only Cape Town</div>
      <div style="color:#F8FAFC;font-size:22px;font-weight:700;letter-spacing:-0.5px;">{title}</div>
      <div style="color:#64748B;font-size:13px;margin-top:4px;">{subtitle}</div>
    </td>
    <td align="right" style="vertical-align:top;">
      <div style="background:#1E3A5F;border-radius:8px;padding:8px 14px;display:inline-block;">
        <div style="color:#60A5FA;font-size:10px;letter-spacing:1px;text-transform:uppercase;">Augos ID</div>
        <div style="color:#F8FAFC;font-size:16px;font-weight:700;">8323</div>
      </div>
    </td>
  </tr></table>
</td></tr>

<!-- BODY -->
<tr><td style="background:#1E293B;padding:32px 40px;">
{dev_banner}
{content}
</td></tr>

<!-- FOOTER -->
<tr><td style="background:#0F172A;border-radius:0 0 12px 12px;padding:20px 40px;
  border-top:1px solid #1E293B;">
  <table width="100%"><tr>
    <td style="color:#334155;font-size:11px;">
      Utility Intelligence Manager &nbsp;·&nbsp; Powered by Augos &amp; Open-Meteo
      &nbsp;·&nbsp; EarthCheck Certified Property
    </td>
    <td align="right" style="color:#1E3A5F;font-size:11px;">&copy; {year}</td>
  </tr></table>
</td></tr>

</table>
</td></tr>
</table>
</body></html>"""


def _all_clear_block(weather: Dict) -> str:
    temp = weather.get("temperature", {})
    t_min = temp.get("min_c", "—")
    t_max = temp.get("max_c", "—")
    rain = weather.get("precipitation_total_mm", 0)
    return f"""
<div style="background:#052E16;border:1px solid #16A34A;border-radius:10px;
  padding:24px 28px;text-align:center;margin-bottom:24px;">
  <div style="font-size:32px;margin-bottom:8px;">✅</div>
  <div style="color:#4ADE80;font-size:18px;font-weight:700;margin-bottom:4px;">All Utilities Normal</div>
  <div style="color:#86EFAC;font-size:14px;">No anomalies detected. No action required.</div>
  <div style="color:#4B5563;font-size:12px;margin-top:12px;">
    Cape Town: {t_min}°C – {t_max}°C &nbsp;·&nbsp; Rain: {rain}mm
  </div>
</div>"""


def _finding_block(finding: Dict) -> str:
    sev = finding.get("severity", "normal")
    colour = _SEVERITY_COLOURS.get(sev, "#6B7280")
    icon = _SEVERITY_ICONS.get(sev, "ℹ️")
    headline = finding.get("headline", "")
    action = finding.get("action", "")
    detail = finding.get("detail", {})

    detail_rows = ""
    for k, v in detail.items():
        if isinstance(v, (str, int, float)) and v is not None:
            label = k.replace("_", " ").title()
            detail_rows += f"""
      <tr>
        <td style="color:#64748B;font-size:12px;padding:4px 0;width:45%;">{label}</td>
        <td style="color:#CBD5E1;font-size:12px;padding:4px 0;font-weight:600;">{v}</td>
      </tr>"""

    return f"""
<div style="border-left:3px solid {colour};background:#0F172A;border-radius:0 8px 8px 0;
  padding:16px 20px;margin-bottom:16px;">
  <div style="margin-bottom:8px;">
    <span style="font-size:16px;">{icon}</span>
    <span style="color:#F8FAFC;font-size:15px;font-weight:600;margin-left:8px;">{headline}</span>
  </div>
  {f'<table width="100%" style="margin:8px 0 12px;">{detail_rows}</table>' if detail_rows else ''}
  {f'<div style="background:#1E293B;border-radius:6px;padding:10px 14px;color:#FCD34D;font-size:13px;"><strong>Action:</strong> {action}</div>' if action else ''}
</div>"""


def _findings_section(findings: List[Dict], weather_ctx: Dict) -> str:
    if not findings:
        return _all_clear_block(weather_ctx)

    p1 = [f for f in findings if f.get("severity") == "P1_CRITICAL"]
    p2 = [f for f in findings if f.get("severity") == "P2_WARNING"]
    p3 = [f for f in findings if f.get("severity") in ("P3_INSIGHT", "P3_POSITIVE")]

    html = f"""
<div style="color:#94A3B8;font-size:12px;letter-spacing:1px;text-transform:uppercase;
  font-weight:600;margin-bottom:16px;">
  {len(findings)} Finding{'s' if len(findings) != 1 else ''} Require{'s' if len(findings) == 1 else ''} Attention
</div>"""

    if p1:
        html += '<div style="color:#EF4444;font-size:11px;letter-spacing:1px;text-transform:uppercase;font-weight:600;margin:16px 0 8px;">🔴 Critical</div>'
        for f in p1:
            html += _finding_block(f)

    if p2:
        html += '<div style="color:#F59E0B;font-size:11px;letter-spacing:1px;text-transform:uppercase;font-weight:600;margin:16px 0 8px;">⚠️ Warning</div>'
        for f in p2:
            html += _finding_block(f)

    if p3:
        html += '<div style="color:#3B82F6;font-size:11px;letter-spacing:1px;text-transform:uppercase;font-weight:600;margin:16px 0 8px;">💡 Insights</div>'
        for f in p3:
            html += _finding_block(f)

    return html


def _text_body(persona: str, findings: List[Dict], all_clear: bool) -> str:
    """Plain text fallback for email clients that don't render HTML."""
    lines = [
        f"One & Only Cape Town — Utility Intelligence Report",
        f"Persona: {persona.replace('_', ' ').title()}",
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        "=" * 60,
    ]
    if all_clear:
        lines.append("✅ All utilities normal. No action required.")
    else:
        for f in findings:
            lines += [
                f"\n{_SEVERITY_ICONS.get(f.get('severity',''), '•')} {f.get('headline','')}",
                f"Action: {f.get('action', 'See detail')}",
            ]
    return "\n".join(lines)


# ─── Persona Email Builders ───────────────────────────────────────────────────

def _subject(persona: str, findings: List[Dict], all_clear: bool) -> str:
    now = datetime.utcnow()
    date_str = now.strftime("%-d %b %Y")
    p1_count = sum(1 for f in findings if f.get("severity") == "P1_CRITICAL")

    prefixes = {
        "chief_engineer":        f"[O&O CPT] Morning Brief — {date_str}",
        "general_manager":       f"[O&O CPT] Weekly Summary — {date_str}",
        "financial_controller":  f"[O&O CPT] Financial Report — {now.strftime('%B %Y')}",
        "sustainability_officer": f"[O&O CPT] Sustainability Report — {now.strftime('%B %Y')}",
    }
    base = prefixes.get(persona, f"[O&O CPT] Utility Report — {date_str}")

    if p1_count:
        return f"🔴 {p1_count} Critical Alert{'s' if p1_count > 1 else ''} — " + base
    if not all_clear:
        return "⚠️ " + base
    return "✅ " + base


def _subtitle(persona: str) -> str:
    now = datetime.utcnow()
    subtitles = {
        "chief_engineer":        f"Engineering Brief · {now.strftime('%A, %-d %B %Y · %H:%M')} SAST",
        "general_manager":       f"Executive Summary · {now.strftime('%A, %-d %B %Y')}",
        "financial_controller":  f"Financial Analysis · {now.strftime('%B %Y')}",
        "sustainability_officer": f"EarthCheck KPI Report · {now.strftime('%B %Y')}",
    }
    return subtitles.get(persona, now.strftime("%-d %B %Y"))


# ─── Public Sending Functions (agent tools) ───────────────────────────────────

def send_engineering_brief(point_id: int = 8323) -> Dict[str, Any]:
    """
    Run the full engineering analysis and email the findings to the Chief Engineer.

    Runs ALL engineering checks internally (base load, PF, anomalies, demand,
    meter health). Emails only noteworthy findings. On a normal day, sends a
    one-line 'All clear' to the Chief Engineer.

    Args:
        point_id: Augos Point ID (default: 8323)

    Returns:
        Send result with message ID, findings count, and all_clear status.
    """
    from .analysis_engine import run_engineering_brief as _run
    result = _run(point_id)
    intended = os.getenv("CHIEF_ENGINEER_EMAIL", "")
    if not intended:
        return {"error": "CHIEF_ENGINEER_EMAIL not set in .env"}

    actual, intercepted = _resolve_recipient(intended, "chief_engineer")
    findings = result.get("findings", [])
    all_clear = result.get("all_clear", True)
    weather = result.get("weather_context", {})

    banner = _dev_banner(intended, "chief_engineer") if intercepted else ""
    content = _findings_section(findings, weather)
    html = _html_wrapper(content, "Morning Engineering Brief", _subtitle("chief_engineer"), dev_banner=banner)
    subject = _subject("chief_engineer", findings, all_clear)
    if intercepted:
        subject = f"[DEV → CE] {subject}"
    text = _text_body("chief_engineer", findings, all_clear)

    service = _build_gmail_service()
    msg_result = _send_raw_email(service, actual, subject, html, text)

    return {
        "sent_to": actual,
        "intended_for": intended,
        "dev_mode": intercepted,
        "subject": subject,
        "all_clear": all_clear,
        "findings_count": len(findings),
        "message_id": msg_result.get("id"),
        "checks_run": result.get("checks_run"),
    }


def send_executive_brief(point_id: int = 8323) -> Dict[str, Any]:
    """
    Run the GM's analysis and email only material findings to the General Manager.

    Applies a high significance threshold — the GM only receives a report when
    something genuinely material is found. On most days returns 'All clear'.

    Args:
        point_id: Augos Point ID (default: 8323)

    Returns:
        Send result with message ID, findings count, and all_clear status.
    """
    from .analysis_engine import run_executive_brief as _run
    result = _run(point_id)
    intended = os.getenv("GM_EMAIL", "")
    if not intended:
        return {"error": "GM_EMAIL not set in .env"}

    actual, intercepted = _resolve_recipient(intended, "general_manager")
    findings = result.get("findings", [])
    all_clear = result.get("all_clear", True)
    weather = result.get("weather_context", {})

    banner = _dev_banner(intended, "general_manager") if intercepted else ""
    content = _findings_section(findings, weather)
    html = _html_wrapper(content, "Weekly Utility Summary", _subtitle("general_manager"), dev_banner=banner)
    subject = _subject("general_manager", findings, all_clear)
    if intercepted:
        subject = f"[DEV → GM] {subject}"
    text = _text_body("general_manager", findings, all_clear)

    service = _build_gmail_service()
    msg_result = _send_raw_email(service, actual, subject, html, text)

    return {
        "sent_to": actual,
        "intended_for": intended,
        "dev_mode": intercepted,
        "subject": subject,
        "all_clear": all_clear,
        "findings_count": len(findings),
        "message_id": msg_result.get("id"),
    }


def send_sustainability_report(point_id: int = 8323) -> Dict[str, Any]:
    """
    Run the sustainability analysis and email EarthCheck KPI findings to the Sustainability Officer.

    Checks carbon footprint, YoY consumption trends, and EarthCheck benchmark bands.
    Only surfaces findings that diverge meaningfully from targets or prior year.

    Args:
        point_id: Augos Point ID (default: 8323)

    Returns:
        Send result with message ID, findings count, and all_clear status.
    """
    from .analysis_engine import run_sustainability_brief as _run
    result = _run(point_id)
    intended = os.getenv("SUSTAINABILITY_EMAIL", "")
    if not intended:
        return {"error": "SUSTAINABILITY_EMAIL not set in .env"}

    actual, intercepted = _resolve_recipient(intended, "sustainability_officer")
    findings = result.get("findings", [])
    all_clear = result.get("all_clear", True)
    weather = result.get("weather_context", {})

    banner = _dev_banner(intended, "sustainability_officer") if intercepted else ""
    content = _findings_section(findings, weather)
    html = _html_wrapper(content, "EarthCheck Sustainability Report", _subtitle("sustainability_officer"), dev_banner=banner)
    subject = _subject("sustainability_officer", findings, all_clear)
    if intercepted:
        subject = f"[DEV → SO] {subject}"
    text = _text_body("sustainability_officer", findings, all_clear)

    service = _build_gmail_service()
    msg_result = _send_raw_email(service, actual, subject, html, text)

    return {
        "sent_to": actual,
        "intended_for": intended,
        "dev_mode": intercepted,
        "subject": subject,
        "all_clear": all_clear,
        "findings_count": len(findings),
        "message_id": msg_result.get("id"),
    }


def send_financial_report(point_id: int = 8323) -> Dict[str, Any]:
    """
    Run the financial analysis and email cost findings to the Financial Controller.

    Checks tariff efficiency, billing anomalies, carbon tax exposure, and savings
    opportunities. Only surfaces financially material findings.

    Args:
        point_id: Augos Point ID (default: 8323)

    Returns:
        Send result with message ID, findings count, and all_clear status.
    """
    from .analysis_engine import run_financial_brief as _run
    result = _run(point_id)
    intended = os.getenv("FINANCE_EMAIL", "")
    if not intended:
        return {"error": "FINANCE_EMAIL not set in .env"}

    actual, intercepted = _resolve_recipient(intended, "financial_controller")
    findings = result.get("findings", [])
    all_clear = result.get("all_clear", True)
    weather = result.get("weather_context", {})

    banner = _dev_banner(intended, "financial_controller") if intercepted else ""
    content = _findings_section(findings, weather)
    html = _html_wrapper(content, "Monthly Financial Report", _subtitle("financial_controller"), dev_banner=banner)
    subject = _subject("financial_controller", findings, all_clear)
    if intercepted:
        subject = f"[DEV → FC] {subject}"
    text = _text_body("financial_controller", findings, all_clear)

    service = _build_gmail_service()
    msg_result = _send_raw_email(service, actual, subject, html, text)

    return {
        "sent_to": actual,
        "intended_for": intended,
        "dev_mode": intercepted,
        "subject": subject,
        "all_clear": all_clear,
        "findings_count": len(findings),
        "message_id": msg_result.get("id"),
    }


def send_immediate_alert(
    finding: Dict,
    recipients: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Send a P1 Critical alert immediately to relevant stakeholders.

    Use for time-sensitive situations: suspected water leak, PF < 0.90,
    meter outage, or demand contract breach. Does not wait for the scheduled brief.

    Args:
        finding: A finding dict as produced by the analysis engine (must have headline, action, severity)
        recipients: Optional list of email addresses. Defaults to Chief Engineer + GM.

    Returns:
        Send results for each recipient.
    """
    if recipients is None:
        intended_list = [
            e for e in [
                os.getenv("CHIEF_ENGINEER_EMAIL", ""),
                os.getenv("GM_EMAIL", ""),
            ] if e
        ]
    else:
        intended_list = recipients

    if not intended_list:
        return {"error": "No recipient emails configured. Set CHIEF_ENGINEER_EMAIL and GM_EMAIL in .env"}

    headline = finding.get("headline", "Critical utility alert")
    now = datetime.utcnow()
    subject = f"🔴 IMMEDIATE ALERT — {headline} — {now.strftime('%-d %b %Y %H:%M')} UTC"
    content = _finding_block(finding)
    html_base = _html_wrapper(content, "⚠️ Immediate Alert",
                              f"One & Only Cape Town · {now.strftime('%-d %B %Y %H:%M')} SAST")
    text = f"ALERT: {headline}\nAction: {finding.get('action', '')}"

    service = _build_gmail_service()
    results = []
    for intended in intended_list:
        actual, intercepted = _resolve_recipient(intended, "p1_alert")
        s = (f"[DEV] {subject}") if intercepted else subject
        banner = _dev_banner(intended, "P1 Alert") if intercepted else ""
        html = _html_wrapper(content, "⚠️ Immediate Alert",
                             f"One & Only Cape Town · {now.strftime('%-d %B %Y %H:%M')} SAST",
                             dev_banner=banner)
        try:
            msg = _send_raw_email(service, actual, s, html, text)
            results.append({"intended": intended, "sent_to": actual,
                            "dev_mode": intercepted, "status": "sent",
                            "message_id": msg.get("id")})
        except Exception as exc:
            results.append({"intended": intended, "sent_to": actual,
                           "status": "failed", "error": str(exc)})

    return {"alert_headline": headline, "recipients": results}


def test_email_connection() -> Dict[str, Any]:
    """
    Test the Gmail API connection and send a test email to the delegator address.

    Use this after completing the Gmail API setup to verify everything is working.
    Sends a brief test email to GMAIL_DELEGATE_ADDRESS.

    Returns:
        Connection status, service account info, and test send result.
    """
    try:
        service = _build_gmail_service()
        delegate = os.getenv("GMAIL_DELEGATE_ADDRESS", "")

        content = """
<div style="background:#052E16;border:1px solid #16A34A;border-radius:10px;
  padding:24px;text-align:center;">
  <div style="font-size:28px;margin-bottom:8px;">🎉</div>
  <div style="color:#4ADE80;font-size:18px;font-weight:700;">Gmail API Connected</div>
  <div style="color:#86EFAC;font-size:14px;margin-top:8px;">
    The Utility Manager Agent can now send emails autonomously.<br><br>
    Service account: utility-manager-agent@augos-core-data.iam.gserviceaccount.com
  </div>
</div>"""
        html = _html_wrapper(content, "Connection Test", "Setup verification")
        text = "Gmail API connected. The Utility Manager Agent can now send emails autonomously."

        msg = _send_raw_email(
            service, delegate,
            "✅ Utility Manager — Gmail API Connected",
            html, text
        )

        return {
            "status": "success",
            "sending_as": delegate,
            "test_email_sent_to": delegate,
            "message_id": msg.get("id"),
        }
    except Exception as exc:
        return {
            "status": "failed",
            "error": str(exc),
            "hint": "See knowledge/SETUP_GMAIL_API.md for setup instructions",
        }
