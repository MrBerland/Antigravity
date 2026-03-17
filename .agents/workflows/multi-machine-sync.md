---
description: Sync the Antigravity workspace between MacBook and Mac mini via Git push/pull
---

# Multi-Machine Sync Protocol

This workflow keeps both Antigravity instances (MacBook + Mac mini) aligned via GitHub.
Follow this every time you finish a session or switch machines.

## When to Run

Run this workflow:
- Before switching from MacBook to Mac mini
- After finishing a coding session on either machine
- Before running the HiveMind pipeline on the Mac mini
- If prompted with "your branch is behind origin"

---

## On the ORIGINATING machine (where you just made changes)

### Step 1 — Check what changed
// turbo
```bash
cd /Users/timstevens/Antigravity && git status
```

### Step 2 — Stage all changes
// turbo
```bash
cd /Users/timstevens/Antigravity && git add -A
```

### Step 3 — Commit with a descriptive message
```bash
cd /Users/timstevens/Antigravity && git commit -m "describe what you changed"
```
Examples:
- `"feat: add email classification pipeline"`
- `"fix: update Gmail watch renewal script"`
- `"docs: update workspace map"`
- `"chore: add OEE visualisation"`

### Step 4 — Push to GitHub
// turbo
```bash
cd /Users/timstevens/Antigravity && git push
```

---

## On the RECEIVING machine (mac mini or MacBook)

### Step 5 — Pull latest
// turbo
```bash
cd /Users/timstevens/Antigravity && git pull
```

### Step 6 — Restart services if code changed
```bash
# Set NVM node on PATH (required on Mac mini — npm/pm2 not in default PATH)
export PATH="/Users/timstevens/.nvm/versions/node/v24.13.0/bin:$PATH"

# Only needed if hive-mind-ui source changed
cd /Users/timstevens/Antigravity/hive-mind-ui && npm install && npm run build && pm2 restart hive-mind-ui

# Only needed if HiveMind Python scripts changed
# (scripts run fresh each time — no restart needed)
echo "Python scripts updated — no restart needed"
```

---

## Important Notes

- **Never commit credentials** — `HiveMind/credentials/` is in `.gitignore`. Transfer the `hive-mind-admin.json` via AirDrop or SCP separately if setting up a new machine.
- **Conflict resolution** — if git pull reports conflicts, always prefer the newer machine's changes: `git checkout --theirs <file> && git add <file>`
- **Large files** — screenshots and binary files from the report-audit are excluded from git. They live only on the originating machine.
- **Mac mini is the server** — run the pipeline, cron jobs, and pm2 from there. Use MacBook only for editing code.

---

## Quick Status Check

To verify both machines are in sync:

```bash
cd /Users/timstevens/Antigravity
git log --oneline -5       # See recent commits
git status                  # Should show "nothing to commit"
git fetch && git status     # Shows if remote has newer commits
```

---

## If a Machine Was Offline

If the Mac mini was offline (power outage, travel) and missed commits:

```bash
# On Mac mini after reconnecting
cd /Users/timstevens/Antigravity
git fetch origin
git log HEAD..origin/main --oneline   # See what you missed
git pull                               # Apply all missed commits
```
