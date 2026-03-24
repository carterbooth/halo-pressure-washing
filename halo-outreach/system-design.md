# Halo Pressure Washing - Outreach System Design

## Overview
Automated cold email outreach + lead management system for Halo Pressure Washing

## Components

### 1. Email Templates
- Multiple variations per audience type (homeowners, property managers, HOAs, real estate agents)
- Personalized with recipient name, street, neighborhood
- Different angles/hooks to avoid spam filters
- All sound human, local, professional

### 2. Target Lists
- Homeowners in nice neighborhoods (Raleigh, Holly Springs, Fuquay, Apex, Cary, Garner, Angier)
- Property management companies
- HOA board contacts
- Real estate agents in service area

### 3. Send Scheduler
- Business hours only:
  - Homeowners: 9 AM - 7 PM
  - B2B (property managers, HOAs): 8 AM - 5 PM
  - Real estate agents: 9 AM - 6 PM
- Staggers sends throughout day (looks organic)
- Never Sundays
- Volume: 75-100/day initially, ramp to 150+

### 4. Inbox Monitor
- Cron job runs every 30 minutes
- Reads new emails from Gmail
- Categorizes: lead inquiry, out-of-office, unsubscribe, spam complaint, interested, not interested
- Routes to appropriate handler

### 5. Lead Qualification Bot
- Asks qualifying questions:
  - Property address
  - Services needed (house, driveway, patio, etc.)
  - House material (vinyl, brick, painted brick, stucco)
  - Preferred timeline
  - Any specific concerns/requests
- Natural conversation flow
- Escalates to Carter if confused or complex

### 6. Estimate Generator
- Pulls address, calculates scope
- Uses Google Maps to estimate square footage if needed
- Applies pricing rules from halo-pressure-washing.md
- Generates professional estimate matching Canva template format
- Includes logo, payment terms, availability

### 7. Booking System
- Offers Tuesday/Wednesday availability
- Confirms jobs into Google Calendar
- Sends Carter notification for confirmed bookings

## File Structure
```
halo-outreach/
├── system-design.md (this file)
├── templates/
│   ├── homeowners.md (5-7 variations)
│   ├── property-managers.md
│   ├── hoa-boards.md
│   ├── real-estate-agents.md
├── targets/
│   ├── homeowners.csv
│   ├── property-managers.csv
│   ├── hoa-contacts.csv
│   ├── real-estate-agents.csv
├── scripts/
│   ├── send-batch.sh (sends daily batch)
│   ├── monitor-inbox.sh (checks for replies)
│   ├── qualify-lead.sh (handles back-and-forth)
│   ├── generate-estimate.sh (creates quotes)
├── state/
│   ├── sent-log.json (tracks who we've emailed)
│   ├── active-leads.json (ongoing conversations)
│   ├── conversions.json (won jobs)
```

## Workflow

### Outbound Flow
1. Cron triggers send-batch.sh at 9 AM
2. Script pulls next batch from targets (75-100 emails)
3. Selects random template variation for each recipient
4. Personalizes with name/location
5. Sends via himalaya CLI
6. Logs to sent-log.json
7. Repeats throughout day with staggered timing

### Inbound Flow
1. Cron runs monitor-inbox.sh every 30 min
2. Checks Gmail for new messages
3. Identifies replies to our cold emails
4. Routes to qualify-lead.sh
5. Bot asks qualifying questions
6. Once qualified → generate-estimate.sh
7. Sends estimate + availability
8. If accepted → books to calendar, notifies Carter

## Success Metrics
- Open rate target: 30%+
- Reply rate target: 3-5%
- Conversion target: 10% of replies → jobs
- Goal: 2-3 booked jobs per week from cold outreach

## Safety / Compliance
- Unsubscribe handling (immediate removal from lists)
- Spam complaint monitoring (pause sends if complaints spike)
- Volume throttling (don't burn the domain)
- CAN-SPAM compliant footers

## Next Steps
1. ✅ Write email templates
2. ✅ Build target lists
3. ✅ Create automation scripts
4. ✅ Set up cron jobs
5. 🔄 Get Carter's approval on templates
6. 🚀 Go live
