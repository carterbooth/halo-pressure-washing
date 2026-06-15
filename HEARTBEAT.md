# Heartbeat Tasks

## Check for pending leads
- Check backend for new pending leads: `GET https://contractor-portal-backend.vercel.app/api/leads/pending`
- Compare against `memory/lead-approval-state.json` to find NEW leads not yet notified
- **ONLY send Telegram notification if there are NEW leads** (don't notify if no new leads)
- After notifying, update `memory/lead-approval-state.json` with the notified lead IDs
- Format: See `memory/lead-approval-workflow.md` for notification template

**Important:** Stay silent if no new pending leads exist. Only notify once per lead.
