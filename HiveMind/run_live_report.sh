#!/bin/bash
# Helper script to run the live reporter

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./run_live_report.sh <POINT_ID> <BEARER_TOKEN>"
    exit 1
fi

POINT=$1
TOKEN=$2
OUT_FILE="report_${POINT}_$(date +%Y%m%d).json"

echo "Running Live Report for Point: $POINT..."
python3 src/agents/reporting/live_reporter.py --point "$POINT" --token "$TOKEN" --out "$OUT_FILE"
