#!/bin/bash

export PATH=$PATH:$HOME/google-cloud-sdk/bin

# Configuration

# Configuration
PROJECT_ID="augos-core-data"
TOPIC_NAME="projects/$PROJECT_ID/topics/gmail-ingest-topic"

echo "🔌 Configuring Gmail Push Notifications..."

# 1. Get Access Token from local gcloud (ADC)
ACCESS_TOKEN=$(gcloud auth application-default print-access-token --scopes=https://www.googleapis.com/auth/gmail.modify)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "❌ Error: Could not get access token. Run 'gcloud auth login' first."
    exit 1
fi

# 2. Call Gmail watch() API
echo "calling users.watch() for 'me'..."

RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"labelIds\": [\"INBOX\"], 
    \"topicName\": \"$TOPIC_NAME\",
    \"labelFilterAction\": \"include\"
  }" \
  "https://gmail.googleapis.com/gmail/v1/users/me/watch")

# 3. Check Result
if [[ $RESPONSE == *"historyId"* ]]; then
    echo "✅ SUCCESS! Gmail is now watching."
    echo "Response: $RESPONSE"
else
    echo "❌ FAILED."
    echo "Response: $RESPONSE"
fi
