# Lead Qualification Script

## Purpose
Handles email replies from cold outreach, qualifies leads, gathers information needed for estimates.

## Conversation Flow

### Initial Reply Detection
When someone replies to our cold email:
1. Check sentiment: interested, maybe, not interested, unsubscribe
2. Route accordingly

### Qualification Questions (if interested)
Ask these in a conversational, natural way - not a form:

**Essential info:**
1. **Address** - "What's the property address?"
2. **Services needed** - "What are you looking to get cleaned? (house, driveway, patio, deck, etc.)"
3. **House material** (if house wash requested) - "Quick question - is your house vinyl siding, brick, or something else? Just helps me price it accurately."
4. **Timeline** - "Any particular timeline you're working with? We typically have Tuesday/Wednesday availability."

**Optional (gather if offered, don't push):**
5. Size context - "Roughly how big is your driveway? (like 1-car, 2-car, 3-car)"
6. Special concerns - "Anything specific you're worried about or want us to focus on?"

### Natural Conversation Style
**Good examples:**
- "Awesome! What's the address and what all are you looking to get cleaned?"
- "Perfect - just need a couple quick details. What's the property address and is it just the driveway or house too?"
- "Great! Real quick - is your house vinyl siding or brick? Makes a difference in how we price it."

**Bad examples (avoid):**
- "Please provide the following information: 1. Address 2. Services..."
- "Thank you for your interest. To proceed, I'll need..."
- "Fill out this form..."

### Handling Objections/Questions

**"How much does it cost?"**
- "Totally fair question! It depends on size and what you need done. If you give me your address and what you want cleaned, I can get you an exact number within a few hours."

**"Can you just give me a ballpark?"**
- "Sure - driveways typically run $150-225, house washes $250-500 depending on size. But I can get you an exact quote if you shoot me your address."

**"I need it done ASAP"**
- "We can usually get jobs done within a few days. What's your address and what needs cleaning? I'll see what we can do."

**"Are you insured?"**
- "Yep, fully insured. Happy to provide proof of insurance with the estimate."

**"Do you have references?"**
- "Absolutely - we've done a bunch of homes in [their area]. I can include some before/after photos with your estimate."

**"What's your availability?"**
- "We typically have Tuesday and Wednesday openings, but we're flexible if you need a specific day. What works best for you?"

### When to Generate Estimate
Once you have:
- ✅ Address
- ✅ Services needed (house/driveway/patio/deck)
- ✅ House material (if applicable)

Generate estimate using `/Users/carterbooth/.openclaw/workspace/halo-outreach/scripts/generate-estimate.sh`

### When to Escalate to Carter
- Complex requests (commercial properties, unusual surfaces)
- Price negotiations beyond standard discounts
- Scheduling conflicts
- Technical questions you're unsure about
- Angry/upset customers

### Unsubscribe Handling
If someone says:
- "Not interested"
- "Remove me"
- "Unsubscribe"
- "Stop emailing me"

Response: "No problem - you're removed from our list. Sorry to bother you!"

Then mark them in state/unsubscribed.json (never email again)

### Follow-Up Timing
- Send estimate immediately after gathering info
- If no response to estimate in 3 days → gentle follow-up: "Hey [name], just wanted to check if you had any questions about the estimate I sent?"
- If no response after follow-up → mark as cold lead, no more contact

### Success Metrics
- Response rate to qualification questions: >80%
- Info gathered in <3 back-and-forth exchanges: >70%
- Escalation rate: <10%
