# Estimate Generator Logic

## Purpose
Creates professional estimates matching Carter's Canva template format, with pricing based on scope and materials.

## Pricing Rules (from halo-pressure-washing.md)

### Minimums
- **Absolute minimum job:** $150
- Will not quote below this under any circumstances

### Driveways (standalone)
- Small (300-400 sqft): $150
- Standard 2-car (500-700 sqft): $175-$225
- Large 3-car/long drive (800+ sqft): $275-$350
- **Estimation:** Use $0.30/sqft as baseline, min $150

### House Washing
- Small/medium vinyl home (1500-2000 sqft): $250-$350
- Large vinyl 2-story (2500-3500 sqft): $400-$500
- **Painted brick or stucco:** +$150 upcharge (solution dries fast, more labor)
- **Regular brick:** Standard rate (note in estimate: "will work in sections")

### Patios/Decks
- Standard back patio (200-400 sqft): $100-$150
- Large/complex patio (500+ sqft): $150-$200
- **Estimation:** Use $0.25-$0.40/sqft

### Package Deals
- **Driveway + House + Patio:**
  - Small/medium vinyl combo: $400-$500
  - Large vinyl 2-story combo: $550-$650
  - Add painted brick/stucco: +$150

### Calculation Strategy
1. Identify services requested
2. Estimate square footage (Google Maps satellite view if needed)
3. Apply per-sqft rates
4. Check against minimum ($150)
5. Add material upcharges (painted brick/stucco)
6. Round to nearest $25 (looks cleaner: $375 not $387)

## Estimate Format

### Header
```
HALO PRESSURE WASHING AND EXTERIORS
6017 Burt Rd, Fuquay Varina, NC 27526
(910) 538-6552
info@halopressurewashing.com

PROFESSIONAL SERVICE BID
```

### Customer Info
```
CUSTOMER: [Name]
ADDRESS: [Property Address]
DATE: [Current Date]
ESTIMATE VALID: 30 days
```

### Scope of Work Table
```
DESCRIPTION                          | QTY  | UNIT PRICE | LINE TOTAL
------------------------------------|------|------------|------------
House Wash - Vinyl Siding           | 1    | $400.00    | $400.00
Driveway Pressure Wash (2-car)      | 1    | $200.00    | $200.00
Back Patio Cleaning                 | 1    | $125.00    | $125.00
                                    |      |            |
                                    |      | SUBTOTAL:  | $725.00
                                    |      | TOTAL:     | $725.00
```

### Notes Section
```
NOTES:
- Estimate is contingent upon use of onsite water supply
- All surfaces will be soft-washed to prevent damage
- [Material-specific notes, e.g., "Painted brick requires additional care - solution applied in small sections"]

PAYMENT:
Balance due upon completion
Accepted: Cash, Check, Venmo, Zelle, CashApp

AVAILABILITY:
Typical availability: Tuesday & Wednesday
[Or: "Can schedule as early as [next Tuesday]"]

Questions? Call or text Carter at (910) 538-6552
```

### Email Body (when sending estimate)
```
Hi [Name],

Thanks for reaching out! Here's your estimate for [services] at [address]:

[Formatted estimate text above]

We're currently scheduling jobs for [next week/this week] - I have Tuesday afternoon or Wednesday morning available if either of those work for you.

Let me know if you have any questions or want to move forward!

Best,
Carter
Halo Pressure Washing
(910) 538-6552
```

## Special Cases

### If house material unknown
- Default to vinyl pricing
- Note in estimate: "Pricing assumes vinyl siding - may adjust if different material"

### If square footage unclear
- Use conservative (higher) estimate
- Note: "Estimate based on [X sqft] - final price confirmed at property"

### If requesting services we don't normally do
- Escalate to Carter
- Or politely decline: "We typically focus on house/driveway/patio work - I'd recommend [other company] for that type of job"

### If price seems too low (<$150)
- Bundle with another service: "For driveways that small, we typically recommend adding the sidewalk or front porch too - we're already there anyway. Would bring the total to $150."
- Or decline politely: "Our minimum is $150 since we're driving out from Fuquay - might not be the most cost-effective option for such a small job"

### If requesting immediate/rush service
- Check Carter's availability (via calendar or escalate)
- Can offer +$50 rush fee for same-day/next-day if desperate

## Quality Checks Before Sending
- ✅ Total is >=$150
- ✅ Line items add up correctly
- ✅ Material upcharges applied (painted brick/stucco)
- ✅ Customer name and address correct
- ✅ Services match what they requested
- ✅ Email tone is professional but friendly
- ✅ Includes availability (Tuesday/Wednesday)
- ✅ Includes payment options

## Success Metrics
- Estimate accuracy (no major revisions needed): >90%
- Quote-to-job conversion: Target 10-15%
- Average job value: Target $300-500
