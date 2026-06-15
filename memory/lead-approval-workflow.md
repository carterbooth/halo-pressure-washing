# Lead Approval Workflow

## Overview
Homeowners submit leads → Leads saved as "pending" → Carter approves/rejects → Approved leads go live

## API Endpoints
- `GET https://contractor-portal-backend.vercel.app/api/leads/pending` - Get pending leads
- `POST https://contractor-portal-backend.vercel.app/api/leads/approve/:id` - Approve a lead
- `POST https://contractor-portal-backend.vercel.app/api/leads/reject/:id` - Reject/delete a lead

## Commands
When Carter says:
- **"approve"** or **"approve [lead-id]"** → Call `/api/leads/approve/:id`
- **"reject"** or **"reject [lead-id]"** → Call `/api/leads/reject/:id`

If no lead ID provided, use the most recent pending lead.

## Heartbeat Monitoring
- Check `/api/leads/pending` every ~10 minutes
- Send Telegram notification for new pending leads
- Track notified leads in `memory/lead-approval-state.json` to avoid duplicates

## Notification Format
```
🚨 NEW PENDING LEAD

Lead ID: [id]
Name: [name]
Address: [address]
Phone: [phone]
Email: [email]

Damage: [damage_type]
Urgency: [urgency]
Insurance: [insurance]
Notes: [description]

Tier: [tierLabel]
Price: $[price]

Reply "approve" or "reject"
```

## State Tracking
`memory/lead-approval-state.json`:
```json
{
  "notifiedLeads": ["lead-id-1", "lead-id-2"],
  "lastCheck": "2026-06-15T23:00:00.000Z"
}
```

## Important
- Leads start as "pending" (invisible to contractors)
- Only approved leads appear in contractor portal
- Rejected leads are permanently deleted
- Carter needs mobile access via Telegram (@draco3000bot)
