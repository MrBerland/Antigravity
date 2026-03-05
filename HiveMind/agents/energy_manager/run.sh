#!/bin/bash
# Quick start script for Energy Manager Agent

# Add ADK to PATH
export PATH="$PATH:/Users/timstevens/Library/Python/3.9/bin"

# Move to agent directory
cd "$(dirname "$0")"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "Please create one from the example:"
    echo "  cp .env.example .env"
    echo "Then add your AUGOS_COOKIES"
    exit 1
fi

# Load environment variables
set -a
source .env
set +a

# Check cookies
if [ -z "$AUGOS_COOKIES" ]; then
    echo "⚠️  AUGOS_COOKIES not set!"
    echo "Please edit .env and add your cookies from the browser"
    exit 1
fi

echo "🔋 Starting Energy Manager Agent..."
echo "   Cookies loaded: ${#AUGOS_COOKIES} characters"
echo ""

# Start ADK web interface from parent directory
cd ..
adk web
