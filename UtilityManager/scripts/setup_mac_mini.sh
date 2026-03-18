#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Mac Mini Setup — Utility Manager Agent
# Run this ONCE on the Mac mini after git pull.
# Installs dependencies, copies credentials, and schedules overnight jobs.
# ─────────────────────────────────────────────────────────────────────────────
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "═══════════════════════════════════════════════════════"
echo "  Utility Manager Agent — Mac Mini Setup"
echo "═══════════════════════════════════════════════════════"
echo ""

# ─── 1. Python dependencies ───────────────────────────────────────────────────
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt --quiet
echo "   ✅ Dependencies installed"
echo ""

# ─── 2. Credentials check ─────────────────────────────────────────────────────
echo "🔐 Checking credentials..."
mkdir -p credentials
if [ -f "credentials/service_account.json" ]; then
    CLIENT_EMAIL=$(python3 -c "import json; d=json.load(open('credentials/service_account.json')); print(d.get('client_email','?'))")
    echo "   ✅ service_account.json present → $CLIENT_EMAIL"
else
    echo "   ⚠️  credentials/service_account.json not found!"
    echo "      Transfer it from MacBook:"
    echo "      scp timstevens@macbook.local:$(pwd)/credentials/service_account.json credentials/"
    echo "      Or: AirDrop the file to Mac mini, then move it here."
fi
echo ""

# ─── 3. .env check ────────────────────────────────────────────────────────────
echo "⚙️  Checking .env..."
if [ -f ".env" ]; then
    echo "   ✅ .env exists"
    # Ensure AUGOS_COOKIES is set
    if grep -q "^AUGOS_COOKIES=$" .env 2>/dev/null || ! grep -q "AUGOS_COOKIES" .env 2>/dev/null; then
        echo "   ⚠️  AUGOS_COOKIES is empty in .env — agent will not be able to fetch data."
        echo "      Extract cookies from live.augos.io and add to .env:"
        echo "      AUGOS_COOKIES=<paste full cookie string>"
    fi
else
    echo "   ⚠️  No .env found — copying from .env.example"
    cp .env.example .env
    echo "   ✅ .env created from example — fill in AUGOS_COOKIES and email fields"
fi
echo ""

# ─── 4. Gmail connection test ─────────────────────────────────────────────────
echo "📧 Testing Gmail API connection..."
RESULT=$(python3 -c "
from utility_manager.tools.email_sender import test_email_connection
import json
r = test_email_connection()
print(r.get('status'), '|', r.get('message_id',''), '|', r.get('error',''))
" 2>/dev/null)
STATUS=$(echo "$RESULT" | cut -d'|' -f1 | tr -d ' ')
if [ "$STATUS" = "success" ]; then
    MSG_ID=$(echo "$RESULT" | cut -d'|' -f2 | tr -d ' ')
    echo "   ✅ Gmail API working — message_id: $MSG_ID"
else
    ERR=$(echo "$RESULT" | cut -d'|' -f3)
    echo "   ❌ Gmail API failed: $ERR"
fi
echo ""

# ─── 5. Cron schedule ─────────────────────────────────────────────────────────
echo "⏰ Setting up overnight cron schedule..."
PYTHON=$(which python3)
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

# Build crontab entries
CRON_JOBS="# Utility Manager Agent — One & Only Cape Town
# Chief Engineer brief — every day at 06:00
0 6 * * * cd $SCRIPT_DIR && $PYTHON -c \"from utility_manager.tools.analysis_engine import run_engineering_analysis; run_engineering_analysis()\" >> $LOG_DIR/engineer.log 2>&1

# GM executive summary — every Monday at 07:00
0 7 * * 1 cd $SCRIPT_DIR && $PYTHON -c \"from utility_manager.tools.analysis_engine import run_executive_analysis; run_executive_analysis()\" >> $LOG_DIR/gm.log 2>&1

# Sustainability report — 1st of each month at 07:30
30 7 1 * * cd $SCRIPT_DIR && $PYTHON -c \"from utility_manager.tools.analysis_engine import run_sustainability_analysis; run_sustainability_analysis()\" >> $LOG_DIR/sustainability.log 2>&1

# Financial report — 1st of each month at 08:00
0 8 1 * * cd $SCRIPT_DIR && $PYTHON -c \"from utility_manager.tools.analysis_engine import run_financial_analysis; run_financial_analysis()\" >> $LOG_DIR/finance.log 2>&1

# Anomaly watchdog — every 2 hours (overnight focus)
0 */2 * * * cd $SCRIPT_DIR && $PYTHON -c \"from utility_manager.tools.anomaly_detection import run_anomaly_check; run_anomaly_check()\" >> $LOG_DIR/anomaly.log 2>&1
"

# Write to a temp file and install
TMPFILE=$(mktemp)
crontab -l 2>/dev/null | grep -v "Utility Manager Agent" | grep -v "utility_manager" > "$TMPFILE" || true
echo "$CRON_JOBS" >> "$TMPFILE"
crontab "$TMPFILE"
rm "$TMPFILE"

echo "   ✅ Cron jobs installed:"
echo "      06:00 daily      — Chief Engineer brief"
echo "      07:00 Monday     — GM executive summary"
echo "      07:30 1st/month  — Sustainability report"
echo "      08:00 1st/month  — Financial report"
echo "      Every 2 hours    — Anomaly watchdog"
echo ""

# ─── 6. Summary ───────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════════"
echo "  Setup complete. Verify cron with: crontab -l"
echo "  Logs will appear in: $LOG_DIR/"
echo "  Monitor status:      tail -f $LOG_DIR/engineer.log"
echo "═══════════════════════════════════════════════════════"
