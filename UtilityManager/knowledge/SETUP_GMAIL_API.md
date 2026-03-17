# Gmail API Setup Guide
## Service Account + Domain-Wide Delegation
### For: Utility Manager Agent — One & Only Cape Town

This is a one-time setup. Once complete, the agent sends email autonomously with no passwords and no manual credential rotation.

---

## Step 1 — Enable Gmail API in Google Cloud

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Select project: **`augos-core-data`**
3. Navigate to **APIs & Services → Library**
4. Search for **"Gmail API"** → Click **Enable**

---

## Step 2 — Create a Service Account

1. Go to **IAM & Admin → Service Accounts**
2. Click **+ Create Service Account**
3. Fill in:
   - **Name:** `Utility Manager Agent`
   - **ID:** `utility-manager-agent` (auto-filled)
   - **Description:** `Sends utility intelligence reports for One & Only Cape Town`
4. Click **Create and Continue**
5. Skip the optional role and user access steps → Click **Done**

---

## Step 3 — Generate a JSON Key

1. Click on the newly created service account
2. Go to the **Keys** tab
3. Click **Add Key → Create new key**
4. Choose **JSON** → Click **Create**
5. The file downloads automatically — **move it to:**
   ```
   /Users/timstevens/Antigravity/UtilityManager/credentials/service_account.json
   ```

> ⚠️ This file is in `.gitignore` and will never be committed to version control.

---

## Step 4 — Note the Client ID

1. In the service account details page, find the **Unique ID (Client ID)** — a long number like `105234567890123456789`
2. Copy this number — you'll need it in Step 6.

---

## Step 5 — Choose a Delegator Gmail Account

The service account needs to impersonate an existing Gmail/Workspace user to send email. Choose one:

**Option A — Use your own account** `tim@yourdomain.com`
- Emails appear to come from your address
- Simplest

**Option B — Create a Gmail alias on your account**
- In Gmail → Settings → Accounts → "Send mail as" → Add `utility-agent@yourdomain.com`
- Emails appear from the agent's address
- Still uses your account's Gmail quota

**Option C — Use a Google Group**
- Create a Group `utility-agent@yourdomain.com`
- Make your account the manager
- Service account impersonates you but sends from the Group alias

Add your chosen delegator address to `.env`:
```
GMAIL_DELEGATE_ADDRESS=tim@yourdomain.com
```

---

## Step 6 — Add Domain-Wide Delegation (Workspace Admin)

> This step requires Google Workspace **Super Admin** access.

1. Go to [admin.google.com](https://admin.google.com)
2. Navigate to **Security → Access and data control → API controls**
3. Click **Manage Domain Wide Delegation**
4. Click **Add new**
5. Fill in:
   - **Client ID:** *(the Unique ID from Step 4)*
   - **OAuth Scopes:** `https://www.googleapis.com/auth/gmail.send`
6. Click **Authorize**

---

## Step 7 — Update `.env`

```bash
# Gmail API (Service Account + Domain-Wide Delegation)
GMAIL_SERVICE_ACCOUNT_PATH=credentials/service_account.json
GMAIL_DELEGATE_ADDRESS=tim@yourdomain.com    # account the SA impersonates

# Email Recipients
CHIEF_ENGINEER_EMAIL=engineer@oneandonlycapetown.com
GM_EMAIL=gm@oneandonlycapetown.com
FINANCE_EMAIL=finance@oneandonlycapetown.com
SUSTAINABILITY_EMAIL=sustainability@oneandonlycapetown.com

# From name shown on emails
EMAIL_FROM_NAME=Utility Intelligence Manager | One & Only Cape Town
```

---

## Step 8 — Test

```bash
cd /Users/timstevens/Antigravity/UtilityManager
python3 -c "from utility_manager.tools.email_sender import test_email_connection; test_email_connection()"
```

Expected output:
```
✅ Gmail API connected successfully
✅ Service account: utility-manager-agent@augos-core-data.iam.gserviceaccount.com
✅ Delegating as: tim@yourdomain.com
✅ Test email sent to: tim@yourdomain.com
```

---

## How It Works (Architecture)

```
Agent runs analysis
      ↓
Significance filter → noteworthy findings only
      ↓
email_sender.py formats HTML email per persona
      ↓
Google OAuth2 service account credentials
      ↓  (impersonates delegator, no password)
Gmail API (users.messages.send)
      ↓
Email delivered from delegator's account
```

---

## Quota & Limits

| Limit | Value |
|-------|-------|
| Gmail API send limit | 1 billion messages/day (service account) |
| Per-user sending quota | 2,000 emails/day (Google Workspace) |
| Agent expected volume | ~10–15 emails/day maximum |

No quota concerns for this use case.

---

## Troubleshooting

**`Delegation denied for user`**
→ Domain-wide delegation not yet propagated. Wait 15–30 minutes after Step 6.

**`Service account JSON not found`**
→ Check `GMAIL_SERVICE_ACCOUNT_PATH` in `.env` and that the file exists at that path.

**`Gmail API not enabled`**
→ Repeat Step 1.
