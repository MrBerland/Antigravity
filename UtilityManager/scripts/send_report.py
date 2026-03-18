#!/usr/bin/env python3
"""
Report Runner — Analysis → HTML Email
======================================
Runs the analysis engine for a given persona, formats findings as HTML,
and sends via Gmail API.

Usage:
    python3 scripts/send_report.py --persona chief_engineer
    python3 scripts/send_report.py --persona general_manager
    python3 scripts/send_report.py --persona sustainability_officer
    python3 scripts/send_report.py --persona financial_controller
    python3 scripts/send_report.py --all     # Fire all 4 reports
"""
import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent dir to path so imports work whether run from scripts/ or root
sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from utility_manager.tools.analysis_engine import (
    run_engineering_brief,
    run_executive_brief,
    run_sustainability_brief,
    run_financial_brief,
)
from utility_manager.tools.email_sender import (
    _build_gmail_service,
    _send_raw_email,
    _html_wrapper,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

POINT_ID = int(os.getenv("AUGOS_PRIMARY_POINT_ID", "8323"))
DEV_EMAIL = os.getenv("DEV_EMAIL", "tim@augos.io")
DEV_MODE  = os.getenv("DEV_MODE", "true").lower() == "true"

PERSONAS = {
    "chief_engineer": {
        "fn":         run_engineering_brief,
        "label":      "Chief Engineer",
        "icon":       "🔧",
        "accent":     "#16A34A",
        "accent_bg":  "#052E16",
        "recipient_env": "CHIEF_ENGINEER_EMAIL",
    },
    "general_manager": {
        "fn":         run_executive_brief,
        "label":      "General Manager",
        "icon":       "📊",
        "accent":     "#2563EB",
        "accent_bg":  "#0A1628",
        "recipient_env": "GM_EMAIL",
    },
    "sustainability_officer": {
        "fn":         run_sustainability_brief,
        "label":      "Sustainability",
        "icon":       "🌿",
        "accent":     "#059669",
        "accent_bg":  "#022C22",
        "recipient_env": "SUSTAINABILITY_EMAIL",
    },
    "financial_controller": {
        "fn":         run_financial_brief,
        "label":      "Financial",
        "icon":       "💰",
        "accent":     "#D97706",
        "accent_bg":  "#1C1005",
        "recipient_env": "FINANCE_EMAIL",
    },
}

SEVERITY_STYLE = {
    "P1_CRITICAL": ("🔴", "#FEE2E2", "#991B1B", "CRITICAL"),
    "P2_WARNING":  ("🟡", "#FEF3C7", "#92400E", "WARNING"),
    "P3_INSIGHT":  ("🔵", "#EFF6FF", "#1E40AF", "INSIGHT"),
    "P3_POSITIVE": ("🟢", "#F0FDF4", "#166534", "POSITIVE"),
}


def _finding_html(finding: dict) -> str:
    sev = finding.get("severity", "P3_INSIGHT")
    icon, bg, border, label = SEVERITY_STYLE.get(sev, ("⚪", "#F9FAFB", "#374151", sev))
    headline = finding.get("headline", "")
    action   = finding.get("action", "")
    detail   = finding.get("detail", {})

    detail_rows = ""
    for k, v in (detail or {}).items():
        if v is not None:
            key_label = k.replace("_", " ").title()
            detail_rows += f"""
            <tr>
              <td style="padding:3px 8px;color:#6B7280;font-size:12px;">{key_label}</td>
              <td style="padding:3px 8px;font-size:12px;font-weight:500;">{v}</td>
            </tr>"""

    return f"""
    <div style="margin:16px 0;padding:16px;background:{bg};border-left:4px solid {border};border-radius:6px;">
      <div style="font-size:11px;font-weight:700;color:{border};letter-spacing:0.05em;margin-bottom:6px;">
        {icon} {label} — {finding.get("category","")}
      </div>
      <div style="font-size:15px;font-weight:600;color:#111827;margin-bottom:8px;">{headline}</div>
      {"<table style='width:100%;margin-bottom:8px;border-collapse:collapse;'>" + detail_rows + "</table>" if detail_rows else ""}
      <div style="font-size:13px;color:#374151;padding:8px;background:rgba(0,0,0,0.03);border-radius:4px;">
        <strong>Action:</strong> {action}
      </div>
    </div>"""


def _format_report(persona: str, result: dict, cfg: dict) -> tuple[str, str, str]:
    """Returns (subject, html_body, plain_text)."""
    now       = datetime.now()
    date_str  = now.strftime("%A, %-d %B %Y")
    label     = cfg["label"]
    icon      = cfg["icon"]
    accent    = cfg["accent"]
    accent_bg = cfg["accent_bg"]
    site_name = "One & Only Cape Town"

    findings       = result.get("findings", [])
    summary        = result.get("findings_summary", {})
    all_clear      = result.get("all_clear", True)
    weather        = result.get("weather_context", {})
    checks_run     = result.get("checks_run", 0)
    errors         = result.get("errors") or []

    p1 = summary.get("p1_critical", 0)
    p2 = summary.get("p2_warning", 0)
    p3 = summary.get("p3_insight", 0)

    # Subject line
    if all_clear:
        subject = f"{icon} {site_name} — All Clear | {label} Brief | {date_str}"
    elif p1 > 0:
        subject = f"🔴 ACTION REQUIRED — {site_name} | {label} | {p1} Critical | {date_str}"
    else:
        subject = f"{icon} {site_name} — {p2} Finding{'s' if p2!=1 else ''} | {label} Brief | {date_str}"

    # Plain text
    plain = f"{site_name} — {label} Utility Brief\n{date_str}\n\n"
    if all_clear:
        plain += "✅ All utilities within normal parameters. No action required.\n"
    else:
        for f in findings:
            plain += f"{'🔴' if f.get('severity')=='P1_CRITICAL' else '🟡'} {f.get('headline','')}\n"
            plain += f"   Action: {f.get('action','')}\n\n"

    # Status block
    if all_clear:
        status_html = f"""
        <div style="background:{accent_bg};border:1px solid {accent};border-radius:10px;
             padding:24px;text-align:center;margin-bottom:24px;">
          <div style="font-size:32px;margin-bottom:8px;">✅</div>
          <div style="color:{accent};font-size:18px;font-weight:700;">All Clear</div>
          <div style="color:#9CA3AF;font-size:13px;margin-top:6px;">
            {checks_run} checks run — all utilities within normal parameters.
          </div>
        </div>"""
    else:
        badges = (
            (f"🔴 {p1} Critical" if p1 else "") + "  " +
            (f"🟡 {p2} Warning"  if p2 else "") + "  " +
            (f"🔵 {p3} Insight"  if p3 else "")
        ).strip()
        status_html = f"""
        <div style="background:#1F2937;border:1px solid #374151;border-radius:10px;
             padding:20px;text-align:center;margin-bottom:24px;">
          <div style="color:#F9FAFB;font-size:16px;font-weight:700;margin-bottom:8px;">
            {len(findings)} Finding{'s' if len(findings)!=1 else ''} Require Attention
          </div>
          <div style="color:#9CA3AF;font-size:13px;">{badges}</div>
        </div>"""

    # Findings
    findings_html = ""
    if findings:
        findings_html = "<h3 style='color:#F9FAFB;font-size:14px;font-weight:600;margin:24px 0 8px;'>FINDINGS</h3>"
        for f in findings:
            findings_html += _finding_html(f)

    # Weather
    weather_html = ""
    t_min = weather.get("temp_min_c")
    t_max = weather.get("temp_max_c")
    rain  = weather.get("precipitation_mm")
    if t_min is not None:
        weather_html = f"""
        <div style="margin-top:16px;padding:10px 14px;background:#1F2937;border-radius:6px;
             font-size:12px;color:#9CA3AF;">
          🌤 Cape Town: {t_min:.0f}°C – {t_max:.0f}°C
          {f' · {rain:.1f}mm rain' if rain else ''}
        </div>"""

    # Dev banner
    dev_banner = ""
    if DEV_MODE:
        dev_banner = """
        <div style="background:#7C3AED;color:white;text-align:center;padding:8px;
             font-size:12px;font-weight:600;border-radius:6px;margin-bottom:16px;">
          🧪 DEV MODE — Reports redirected to developer. Not sent to hotel team.
        </div>"""

    # Error notice
    error_html = ""
    if errors:
        err_list = "".join(f"<li>{e}</li>" for e in errors)
        error_html = f"""
        <div style="margin-top:16px;padding:12px;background:#FEF3C7;border-radius:6px;
             font-size:12px;color:#92400E;">
          ⚠️ Some checks failed: <ul style='margin:4px 0;padding-left:20px;'>{err_list}</ul>
        </div>"""

    content = f"""
    {dev_banner}
    <div style="text-align:center;margin-bottom:20px;">
      <div style="font-size:24px;margin-bottom:4px;">{icon}</div>
      <div style="font-size:11px;font-weight:700;letter-spacing:0.1em;color:#9CA3AF;">
        {site_name.upper()}
      </div>
      <div style="font-size:18px;font-weight:700;color:#F9FAFB;margin:4px 0;">
        {label} Utility Brief
      </div>
      <div style="font-size:12px;color:#6B7280;">{date_str}</div>
    </div>
    {status_html}
    {findings_html}
    {weather_html}
    {error_html}
    <div style="margin-top:24px;padding:12px;border-top:1px solid #374151;
         font-size:11px;color:#6B7280;text-align:center;">
      Utility Intelligence Manager · One &amp; Only Cape Town<br>
      {checks_run} checks · Generated {now.strftime("%H:%M SAST")}
    </div>"""

    html = _html_wrapper(content, f"{label} Utility Brief", site_name)
    return subject, html, plain


def send_report(persona: str) -> dict:
    """Run analysis and send email report for given persona."""
    cfg = PERSONAS.get(persona)
    if not cfg:
        return {"status": "error", "error": f"Unknown persona: {persona}"}

    log.info(f"Running {persona} analysis...")
    try:
        result = cfg["fn"](POINT_ID)
    except Exception as e:
        return {"status": "error", "persona": persona, "error": str(e)}

    subject, html, plain = _format_report(persona, result, cfg)

    # Recipient — always DEV_EMAIL in dev mode
    if DEV_MODE:
        to = DEV_EMAIL
    else:
        to = os.getenv(cfg["recipient_env"], DEV_EMAIL)

    try:
        service = _build_gmail_service()
        msg = _send_raw_email(service, to, subject, html, plain)
        log.info(f"✅ {persona} report sent → {to} (id: {msg.get('id')})")
        return {
            "status": "sent",
            "persona": persona,
            "to": to,
            "subject": subject,
            "message_id": msg.get("id"),
            "findings": result.get("findings_summary"),
            "all_clear": result.get("all_clear"),
        }
    except Exception as e:
        return {"status": "error", "persona": persona, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Send Utility Manager report emails")
    parser.add_argument("--persona", choices=list(PERSONAS.keys()),
                        help="Persona to run report for")
    parser.add_argument("--all", action="store_true", dest="all_personas",
                        help="Run all 4 reports")
    args = parser.parse_args()

    personas_to_run = list(PERSONAS.keys()) if args.all_personas else (
        [args.persona] if args.persona else None
    )

    if not personas_to_run:
        parser.print_help()
        sys.exit(1)

    results = []
    for p in personas_to_run:
        r = send_report(p)
        results.append(r)
        status = "✅" if r.get("status") == "sent" else "❌"
        print(f"{status} {p}: {r.get('subject','') or r.get('error','')}")

    failed = [r for r in results if r.get("status") != "sent"]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
