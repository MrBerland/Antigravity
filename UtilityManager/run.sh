#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# Utility Manager Agent — Start Script
# One & Only Cape Town | Augos Point ID: 8323
# ─────────────────────────────────────────────────────────────────────────────
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load .env
if [ -f .env ]; then
    set -a; source .env; set +a
    echo "✅ Environment loaded from .env"
else
    echo "⚠️  No .env file found. Copy .env.example to .env and configure."
    echo "   cp .env.example .env"
    exit 1
fi

# Activate virtual environment if present
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
elif [ -d "../.venv" ]; then
    source ../.venv/bin/activate
    echo "✅ Virtual environment activated (parent)"
fi

echo ""
echo "🏨 Utility Intelligence Manager"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 One & Only Cape Town — Point ID: 8323"
echo "⚡ Electricity · 💧 Water · 🔥 Gas"
echo "🌿 EarthCheck certified | Net Positive Hospitality"
echo "🌐 Connecting to live.augos.io..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start ADK web interface
adk web
