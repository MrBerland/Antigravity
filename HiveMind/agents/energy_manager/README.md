# Energy Manager Agent

An AI-powered energy management assistant built with Google ADK (Agent Development Kit) 
that provides real-time insights from the Augos Energy Platform.

## Features

- 🔍 **Site Discovery**: Search for sites by name and resolve Point IDs
- 📊 **Comprehensive Reports**: Generate full site analysis with one command
- ⚡ **Power Factor Analysis**: Monitor PF trends and identify penalty risks
- 💰 **Financial Insights**: Review cost breakdowns and invoice data
- 📈 **Consumption Tracking**: Check telemetry status and consumption patterns

## Quick Start

### 1. Install Dependencies

```bash
cd agents/energy_manager
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Augos API token
# Get your token from: https://live.augos.io
```

### 3. Run Locally with ADK

```bash
# From the agents directory
cd /Users/timstevens/Antigravity/HiveMind/agents

# Start the ADK web interface
adk web
```

This will open a local chat interface where you can interact with the Energy Manager.

### 4. Example Conversations

```
You: Give me a report for The Westin
Agent: [Uses resolve_site_id, then generate_site_report]

You: What's the power factor at site 1022?
Agent: [Uses get_power_factor_report and provides analysis]

You: Show me costs for V&A Waterfront last 3 months
Agent: [Uses resolve_site_id, then get_financial_summary]
```

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `resolve_site_id` | Search for sites by name | `search_term: str` |
| `get_site_details` | Get site metadata | `point_id: int` |
| `get_financial_summary` | Cost breakdown & invoices | `point_id: int, months: int` |
| `get_power_factor_report` | PF analysis & recommendations | `point_id: int, months: int` |
| `get_consumption_summary` | Consumption & telemetry status | `point_id: int, days: int` |
| `generate_site_report` | Full comprehensive report | `point_id: int` |

## Deployment to Vertex AI

To deploy this agent to Google Cloud Vertex AI:

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project augos-core-data

# Deploy using ADK
adk deploy --project=augos-core-data --region=us-central1
```

## Project Structure

```
energy_manager/
├── __init__.py      # Package exports
├── agent.py         # Main agent definition
├── tools.py         # API integration tools
├── requirements.txt # Dependencies
├── .env.example     # Environment template
└── README.md        # This file
```

## API Reference

This agent connects to the Augos Energy Platform API:
- Base URL: `https://live.augos.io/api/v1`
- Authentication: Bearer token (set via `AUGOS_API_TOKEN`)

### Key Endpoints Used

- `/measurement/points/list` - Site discovery
- `/measurement/points/point` - Site details
- `/cost-breakdown` - Financial data
- `/power-factor-demand` - PF analysis
- `/consumption-breakdown` - Consumption data
- `/bills-verification/bill-list` - Invoice data

## Troubleshooting

### "AUGOS_API_TOKEN not set"
Ensure you've created a `.env` file with your token:
```bash
export AUGOS_API_TOKEN="your_token_here"
```

### "No data found"
This usually means:
1. The Point ID doesn't exist
2. No data for the requested time period
3. API connectivity issues

### ADK not found
Install the ADK:
```bash
pip install google-adk
```

## License

Internal use - Augos Energy Platform
