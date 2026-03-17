"""
Auth Manager — Augos Cookie Authentication
==========================================
The Augos API uses a full browser cookie string for authentication.
There is no programmatic login endpoint — you must extract cookies
from a live browser session.

Setup (one-time, takes ~2 minutes):
  1. Log in to https://live.augos.io in Chrome/Safari
  2. Open DevTools (F12) → Network tab
  3. Click any request to /api/v1/
  4. Find the 'Cookie' header in Request Headers
  5. Copy the ENTIRE value (it's a long string)
  6. Paste into .env as: AUGOS_COOKIES=<paste here>

Cookies typically last 7–30 days. Re-extract if you see 401/403 errors.

Alternative (automated extraction):
  python3 scripts/get_session_token.py
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

_CACHE_PATH = Path(__file__).parent.parent.parent / "memory" / "token_cache.json"
_API_BASE   = "https://live.augos.io"


# ─── Cookie retrieval ─────────────────────────────────────────────────────────

def _get_cookies_from_env() -> Optional[str]:
    """Read AUGOS_COOKIES (full cookie string) from environment."""
    cookies = os.getenv("AUGOS_COOKIES", "").strip()
    if cookies and cookies != "your_cookie_string_here":
        return cookies
    return None


def _load_cache() -> Dict:
    if _CACHE_PATH.exists():
        try:
            return json.loads(_CACHE_PATH.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def _save_cache(cache: Dict) -> None:
    _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _CACHE_PATH.write_text(json.dumps(cache, indent=2))


# ─── Public API ───────────────────────────────────────────────────────────────

def get_session_token() -> str:
    """
    Return the Augos cookie string for API authentication.

    Reads AUGOS_COOKIES from .env. Raises ValueError if not configured.

    Raises:
        ValueError: AUGOS_COOKIES not set in .env.
    """
    cookies = _get_cookies_from_env()
    if cookies:
        log.debug("Auth: Using AUGOS_COOKIES from environment")
        return cookies

    raise ValueError(
        "AUGOS_COOKIES is not set in .env.\n"
        "To get your cookie string:\n"
        "  1. Log in to https://live.augos.io\n"
        "  2. Open DevTools (F12) → Network → any /api/v1/ request\n"
        "  3. Copy the entire 'Cookie' request header value\n"
        "  4. Paste into .env as: AUGOS_COOKIES=<value>\n"
        "\nOr run: python3 scripts/get_session_token.py"
    )


def get_headers() -> Dict[str, str]:
    """Return authenticated HTTP headers for all Augos API requests."""
    cookies = get_session_token()
    return {
        "Accept": "application/json, text/plain, */*",
        "Cookie": cookies,
        "Referer": "https://live.augos.io/",
    }


def invalidate_token() -> None:
    """Called on 401/403 — logs a reminder to refresh the cookie string."""
    log.warning(
        "Auth: Received 401/403 from Augos API. "
        "Your session cookies may have expired. "
        "Re-extract and update AUGOS_COOKIES in .env, "
        "or run: python3 scripts/get_session_token.py"
    )


def get_auth_status() -> Dict:
    """Return current auth status without making any API calls."""
    cookies = _get_cookies_from_env()
    configured = cookies is not None
    preview = (cookies[:40] + "...") if configured and len(cookies) > 40 else cookies

    return {
        "auth_mode": "cookie_string",
        "cookies_configured": configured,
        "cookie_preview": preview if configured else None,
        "hint": (
            "Cookies configured. Re-extract if you see 401/403 errors."
            if configured else
            "AUGOS_COOKIES not set. Run: python3 scripts/get_session_token.py"
        ),
    }
