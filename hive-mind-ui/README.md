# Hive Mind Admin Console

The central nervous system for the **Hive Mind** architecture. This application provides observability, governance, and intelligence over the organization's email ingestion pipeline.

## Modules

### 1. Dashboard (`/`)
- Real-time ingestion statistics.
- System health monitoring (Active Users, Blocked Messages).
- Ingestion velocity charts.

### 2. Intelligence Unit (`/emails/intelligence`)
- **Knowledge Graph**: Visualization of top connected entities (Sites, Suppliers, Assets).
- **Recent Semantic Connections**: Live feed of entity resolution events matched by Gemini.
- **Extraction Agent**: Interactive tool to test semantic extraction on specific message IDs.

### 3. Ops War Room (`/emails/ops`)
- **Bottleneck Detector**: Identifies stalled workflows and high-friction threads.
- **Friction Scoring**: Automated prioritization of communications requiring attention.

### 4. Quarantine Inspector (`/emails/quarantine`)
- Raw view of the `staging_raw_emails` ingestion lake.
- Filter by status (Pending, Blocked, Processed).
- Deep link to full thread views.

### 5. Subscription Manager (`/emails/subscriptions`)
- Identifies high-volume senders (newsletters, bots).
- **Unsubscribe Agent**: One-click automated unsubscribe using RFC 8058 (POST) or Mailto fallback.

### 6. Governance (`/emails/governance`)
- Management interface for Global Allow/Block lists.
- Regex pattern matching for security rules.

### 7. Email Thread View (`/emails/thread/[id]`)
- Full HTML thread reconstruction.
- Internal reply capability (acting as the user).

## Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + Lucide Icons
- **Database**: Google BigQuery (Direct Connection)
- **Auth**: Google Service Account (JWT with Domain-Wide Delegation)

## Getting Started

1. **Environment Setup**:
   Ensure `GOOGLE_APPLICATION_CREDENTIALS` matches the path to your Service Account JSON key.

2. **Run Development Server**:
   ```bash
   npm run dev
   ```

3. **Build for Production**:
   ```bash
   npm run build
   npm start
   ```
