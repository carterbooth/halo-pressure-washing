# 🚀 Halo Pressure Washing - Launch Guide

## System Status: READY TO LAUNCH

Your automated lead generation machine is built and ready to go. Here's everything you need to know.

---

## What's Already Running

### ✅ Inbox Monitor (Live Now)
- **What it does:** Checks Gmail every 30 minutes for replies to your cold emails
- **How it works:** 
  - Reads new emails
  - Qualifies leads through natural conversation
  - Gathers address, services needed, house material, timeline
  - Generates professional estimates matching your template
  - Sends quotes with your pricing rules ($150 min, +$150 for painted brick/stucco)
  - Updates lead tracking files
  - Notifies you when jobs are won
- **Runs:** Every 30 minutes, 24/7
- **Check status:** Cron job ID `2348aa58-3279-4ad7-addb-6a82c30cb8ba`

---

## What You Need To Do Before Going Live

### 1. Populate Target Lists ⚠️ CRITICAL

Your email templates are ready, but you need contacts to send to. Add emails to these CSV files:

**Location:** `/Users/carterbooth/.openclaw/workspace/halo-outreach/targets/`

#### homeowners.csv
Format:
```csv
email,first_name,last_name,street_name,neighborhood_name,city
john.smith@example.com,John,Smith,Oak Ridge Lane,Sunset Hills,Raleigh
```

**Where to find homeowners:**
- Facebook neighborhood groups (ask to join, scrape member emails if allowed)
- Nextdoor (search neighborhoods, message homeowners)
- Public property records (Wake County GIS + skip tracing services)
- Door-knock nice neighborhoods, ask for emails instead of leaving hangers

**Target:** 100-200 homeowner emails to start

---

#### property-managers.csv
Format:
```csv
email,first_name,last_name,company_name,property_name,city
sarah.jones@pmcompany.com,Sarah,Jones,Raleigh Property Management,Riverside Apartments,Raleigh
```

**Where to find:**
- Google: "property management companies Raleigh NC"
- Apartment complex websites (look for management contact)
- LinkedIn: search "property manager Raleigh"

**Target:** 30-50 property managers

---

#### hoa-contacts.csv
Format:
```csv
email,first_name,last_name,neighborhood_name,city
board@sunsethillshoa.com,Jennifer,Martinez,Sunset Hills,Raleigh
```

**Where to find:**
- HOA websites (most neighborhoods have one)
- Facebook groups for neighborhoods
- Ask current HOA residents for board contact

**Target:** 20-30 HOA contacts

---

#### real-estate-agents.csv
Format:
```csv
email,first_name,last_name,brokerage,city
michael.chen@kw.com,Michael,Chen,Keller Williams,Raleigh
```

**Where to find:**
- Zillow/Realtor.com agent profiles
- Brokerage websites (Keller Williams, RE/MAX, Coldwell Banker, etc.)
- LinkedIn: "real estate agent Raleigh NC"

**Target:** 40-60 agents

---

### 2. Send Your First Batch

Once you have contacts populated, tell me to send the first batch:

**Command:** "Send the first batch of Halo cold emails"

I'll:
- Pick 75-100 contacts (mixed audience types)
- Select random template variations
- Personalize each email
- Send via Gmail during business hours (9 AM - 7 PM)
- Log everything to state/sent-log.json

---

### 3. Monitor Performance

Check these files to track your campaign:

**state/sent-log.json** - Who you've emailed, when, what template  
**state/active-leads.json** - Leads you're currently qualifying  
**state/conversions.json** - Won jobs, revenue tracking  
**state/unsubscribed.json** - People who opted out (never email again)

---

## How The System Works (Day-to-Day)

### Morning (9 AM)
I send the day's batch of cold emails (75-100), staggered throughout business hours.

### Every 30 Minutes
I check Gmail for replies:
- Interested? → Start qualification conversation
- Have info? → Send estimate
- Accepted? → Notify you, update conversions
- Unsubscribe? → Remove them, apologize

### When You Get A Job
I'll notify you via this chat with:
- Customer name & address
- Services requested
- Quoted price
- Their preferred timeline

You confirm availability, I add to your Google Calendar (future feature).

---

## Sending Strategy

### Volume
- **Week 1:** 75-100 emails/day (conservative, test deliverability)
- **Week 2:** 100-150 emails/day (if no spam complaints)
- **Week 3+:** 150-200 emails/day (full blitz mode)

### Timing
- Homeowners: 9 AM - 7 PM
- B2B (property managers, HOAs): 8 AM - 5 PM
- Real estate agents: 9 AM - 6 PM
- Never Sundays

### Template Rotation
- Each person gets a random template from their audience type
- Never send the same template to the same person twice
- Looks organic, avoids spam filters

---

## Expected Results

Based on industry averages for cold email:

**Open rate:** 30-40% (local, personalized emails perform well)  
**Reply rate:** 3-5% (3-5 people reply per 100 sent)  
**Conversion rate:** 10-15% of replies → jobs

**Example Week 1 Math:**
- Send 500 emails
- Get 15-25 replies
- Close 2-4 jobs
- Revenue: $600-$2000

**Scales up as you send more.**

---

## Safety & Compliance

### Unsubscribes
I handle these automatically:
- Reply: "No problem - you're removed. Sorry to bother you!"
- Add to unsubscribed.json
- Never email them again

### Spam Complaints
If multiple people mark as spam:
- I'll pause sends
- We'll adjust templates or targeting
- Resume once resolved

### Email Deliverability
- Sending from Gmail (good reputation)
- Personalized emails (not bulk blasts)
- Human-written templates (not salesy)
- Should have strong deliverability

---

## Troubleshooting

### "I'm not getting replies"
- Check if emails are landing in spam (ask a friend to check)
- Review templates - too salesy? Not compelling enough?
- Target list quality - are emails valid?

### "People are annoyed"
- Adjust templates to be softer/less aggressive
- Reduce send volume
- Better targeting (nicer neighborhoods only)

### "Inbox monitor isn't working"
- Check cron job status: `openclaw cron list`
- Look for errors in session logs
- Tell me and I'll debug

---

## Next Steps (In Order)

1. ⚠️ **Populate target CSVs with contacts** (100-200 to start)
2. ✅ Tell me: "Send the first batch"
3. ✅ Wait for replies (inbox monitor handles them)
4. ✅ Review estimates I generate (make sure they sound good)
5. ✅ Confirm jobs when they come in
6. ✅ Add more contacts weekly to keep pipeline full

---

## Commands You Can Use

**"Send the first batch"** - Launch initial cold email campaign  
**"Check inbox for replies"** - Manually trigger inbox check  
**"Show me active leads"** - List current conversations  
**"How many emails have we sent?"** - Campaign stats  
**"Add [email] to unsubscribe list"** - Manually block someone  
**"Pause cold email sends"** - Stop outbound temporarily  
**"Resume cold email sends"** - Restart outbound  

---

## Questions?

Just ask me. I'll:
- Help you find contacts
- Adjust templates if needed
- Debug any issues
- Track your performance
- Celebrate when you close jobs

**You built a pressure washing business. I built you a lead machine. Let's fill your calendar.** 🚀

---

*System built: March 23, 2026*  
*Status: Ready to launch*  
*Inbox monitoring: Active*  
*Cold email sending: Waiting for target lists*
