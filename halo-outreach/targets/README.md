# Target Lists

## Overview
This directory contains contact lists for cold email outreach.

## File Format
Each CSV should have these columns:
- `email` (required)
- `first_name` (required)
- `last_name` (optional)
- `street_name` (for homeowners)
- `neighborhood_name` (for homeowners)
- `city` (required)
- `company_name` (for B2B)
- `property_name` (for property managers)

## Files

### homeowners.csv
Homeowners in nice neighborhoods within 30 miles of Fuquay Varina:
- Raleigh
- Holly Springs
- Fuquay Varina
- Apex
- Cary
- Garner
- Angier

**NOT Durham** (outside service area)

Focus on mid-to-high income neighborhoods with nice homes.

### property-managers.csv
Property management companies managing rentals/multi-family in service area.

### hoa-contacts.csv
HOA board members, management companies, neighborhood associations.

### real-estate-agents.csv
Active agents in Raleigh/Wake County area.

## How to Populate

### Option 1: Manual Research
- Google search: "property management companies Raleigh NC"
- HOA directories, neighborhood websites
- Real estate agent listings (Zillow, Realtor.com)
- LinkedIn searches

### Option 2: Data Services (if budget allows)
- Apollo.io
- ZoomInfo
- Local business directories
- MLS data (for agents)

### Option 3: Scraping (legal/ethical only)
- Public HOA websites
- Real estate brokerage listings
- Property management company websites

## Sample Homeowner Entry
```csv
email,first_name,last_name,street_name,neighborhood_name,city
john.smith@example.com,John,Smith,Oak Ridge Lane,Sunset Hills,Raleigh
```

## Sample Property Manager Entry
```csv
email,first_name,last_name,company_name,property_name,city
sarah.jones@pmcompany.com,Sarah,Jones,Raleigh Property Management,Riverside Apartments,Raleigh
```

## Important
- Never email unsubscribed addresses (check state/unsubscribed.json)
- Never email the same person twice (check state/sent-log.json)
- Validate emails before sending (basic format check)
- Remove bounced/invalid emails after each batch
