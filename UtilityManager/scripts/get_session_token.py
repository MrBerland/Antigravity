#!/usr/bin/env python3
"""
Get Augos Session Token
========================
Opens live.augos.io in your browser, waits for you to log in,
then automatically extracts your session token and writes it to .env

Usage:
    python3 scripts/get_session_token.py

What it does:
    1. Opens https://live.augos.io in your default browser
    2. Waits for you to log in manually (you keep your credentials private)
    3. Uses Playwright to read the session token from browser storage
    4. Writes AUGOS_SESSION_ID=<token> to your .env file

Requires Playwright (installed automatically on first run).
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).parent.parent
_ENV_PATH  = _REPO_ROOT / ".env"
_AUGOS_URL = "https://live.augos.io"


def _install_playwright():
    """Install playwright and chromium if not already installed."""
    try:
        import playwright  # noqa
        return True
    except ImportError:
        print("📦 Installing Playwright (one-time)...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        return True


def _update_env(token: str) -> None:
    """Write or update AUGOS_SESSION_ID in .env"""
    if not _ENV_PATH.exists():
        print(f"⚠️  {_ENV_PATH} not found — creating from .env.example")
        example = _REPO_ROOT / ".env.example"
        if example.exists():
            _ENV_PATH.write_text(example.read_text())
        else:
            _ENV_PATH.write_text("")

    content = _ENV_PATH.read_text()
    pattern = r"^AUGOS_SESSION_ID=.*$"
    new_line = f"AUGOS_SESSION_ID={token}"

    if re.search(pattern, content, re.MULTILINE):
        content = re.sub(pattern, new_line, content, flags=re.MULTILINE)
        print("✅ Updated AUGOS_SESSION_ID in .env")
    else:
        # Add after AUGOS_PASSWORD line if present, otherwise append
        if "AUGOS_PASSWORD" in content:
            content = content.replace(
                "\nAUGOS_PASSWORD",
                f"\n# Session token (no password required)\n{new_line}\nAUGOS_PASSWORD"
            )
        else:
            content += f"\n# Augos session token\n{new_line}\n"
        print("✅ Added AUGOS_SESSION_ID to .env")

    _ENV_PATH.write_text(content)


def _extract_token_from_storage(page) -> str | None:
    """Try all known locations for the Augos session token."""
    # Method 1: Session Storage → utsdb → augosportal-sid (primary)
    try:
        raw = page.evaluate("JSON.parse(sessionStorage.getItem('utsdb') || '{}')")
        if isinstance(raw, dict):
            sid = raw.get("augosportal-sid") or raw.get("sid")
            if sid:
                return sid
    except Exception:
        pass

    # Method 2: Local Storage
    try:
        raw = page.evaluate("JSON.parse(localStorage.getItem('utsdb') || '{}')")
        if isinstance(raw, dict):
            sid = raw.get("augosportal-sid") or raw.get("sid")
            if sid:
                return sid
    except Exception:
        pass

    # Method 3: Cookies
    try:
        cookies = page.context.cookies()
        for c in cookies:
            if c["name"] in ("augosportal-sid", "token", "session"):
                return c["value"]
    except Exception:
        pass

    return None


def main():
    print("╔══════════════════════════════════════════════════════╗")
    print("║  Augos Session Token Extractor                       ║")
    print("║  Utility Manager Agent — One & Only Cape Town        ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    _install_playwright()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        print("🌐 Opening https://live.augos.io in a browser window...")
        print("   Log in with your Augos credentials.")
        print("   This script is watching for your session — it will continue automatically.\n")

        browser = pw.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport=None)
        page = context.new_page()
        page.goto(_AUGOS_URL)

        # Wait for login — poll session storage until we find a token
        print("⏳ Waiting for login (timeout: 3 minutes)...")
        token = None
        deadline = time.time() + 180  # 3 min

        while time.time() < deadline:
            time.sleep(2)
            # Check if we've navigated past the login page
            current_url = page.url
            if "/login" in current_url or "/auth" in current_url:
                continue  # Still on login page
            if "live.augos.io" not in current_url:
                continue

            token = _extract_token_from_storage(page)
            if token:
                break
            # Also check if we're logged in by looking for dashboard elements
            try:
                dashboard_visible = page.locator("nav, [data-testid='sidebar'], .sidebar").count() > 0
                if dashboard_visible and not token:
                    # Logged in but token not yet in storage — wait a beat
                    time.sleep(1)
                    token = _extract_token_from_storage(page)
                    if token:
                        break
            except Exception:
                pass

        browser.close()

    if not token:
        print("\n❌ Could not extract session token.")
        print("   Try again, or extract manually:")
        print("   1. Log in to https://live.augos.io")
        print("   2. Open DevTools (F12) → Application → Session Storage")
        print("   3. Click live.augos.io → find 'utsdb' key")
        print("   4. Copy the value of 'augosportal-sid' from the JSON")
        print("   5. Add to .env:  AUGOS_SESSION_ID=<paste here>")
        sys.exit(1)

    print(f"\n✅ Session token found!")
    print(f"   Token: {token[:20]}...{token[-8:]} (truncated for security)")
    print()
    _update_env(token)
    print()
    print("🚀 You're ready. Run the connection test:")
    print("   python3 -c \"")
    print("   from utility_manager.tools.email_sender import test_email_connection")
    print("   import json; print(json.dumps(test_email_connection(), indent=2))\"")


if __name__ == "__main__":
    main()
