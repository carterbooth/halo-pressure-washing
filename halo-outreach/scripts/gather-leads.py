#!/usr/bin/env python3
"""
Lead gathering script for Halo Pressure Washing
Scrapes Google Maps for business contacts with rate limiting
"""

import csv
import json
import time
import re
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random

# Configuration
BASE_DIR = Path(__file__).parent.parent
TARGETS_DIR = BASE_DIR / "targets"
STATE_DIR = BASE_DIR / "state"
LOG_FILE = STATE_DIR / "scraping-log.json"

# Service areas
CITIES = ["Raleigh NC", "Holly Springs NC", "Fuquay Varina NC", "Apex NC", "Cary NC", "Garner NC", "Angier NC"]

# Search queries by business type
QUERIES = {
    "property-managers": [
        "property management company {}",
        "rental property management {}",
        "apartment management {}",
    ],
    "hoa-contacts": [
        "HOA management {}",
        "homeowners association {}",
        "community association {}",
    ],
    "real-estate-agents": [
        "real estate agent {}",
        "realtor {}",
        "real estate broker {}",
    ]
}

# Rate limiting settings
MIN_DELAY = 8  # seconds between requests
MAX_DELAY = 15
REQUEST_TIMEOUT = 10

def log_progress(message, data=None):
    """Log progress to file and console"""
    timestamp = datetime.now().isoformat()
    log_entry = {"timestamp": timestamp, "message": message}
    if data:
        log_entry["data"] = data
    
    print(f"[{timestamp}] {message}")
    
    # Append to log file
    logs = []
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    
    logs.append(log_entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs[-100:], f, indent=2)  # Keep last 100 entries

def extract_email(text):
    """Extract email from text using regex"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def search_google_maps(query):
    """Search Google Maps and extract business info"""
    results = []
    
    # Google Maps search URL
    search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        log_progress(f"Searching: {query}")
        response = requests.get(search_url, headers=headers, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 429:
            log_progress("⚠️ Rate limit hit! Pausing for 60 seconds...")
            time.sleep(60)
            return results
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a simplified scraper - Google Maps HTML is complex
        # In production, you'd want to use Selenium or Google Places API
        # For now, we'll just demonstrate the structure
        
        log_progress(f"Found page for: {query} (manual extraction needed)")
        
    except Exception as e:
        log_progress(f"❌ Error searching {query}: {str(e)}")
    
    return results

def load_existing_contacts(csv_file):
    """Load existing contacts from CSV to avoid duplicates"""
    existing = set()
    if csv_file.exists():
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'email' in row:
                    existing.add(row['email'].lower())
    return existing

def append_to_csv(csv_file, contacts, fieldnames):
    """Append new contacts to CSV file"""
    file_exists = csv_file.exists()
    
    with open(csv_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists or csv_file.stat().st_size == 0:
            writer.writeheader()
        
        for contact in contacts:
            writer.writerow(contact)
    
    log_progress(f"✅ Added {len(contacts)} contacts to {csv_file.name}")

def manual_entry_mode(business_type):
    """Manual entry helper for quickly adding contacts"""
    csv_file = TARGETS_DIR / f"{business_type}.csv"
    
    print(f"\n📝 Manual Entry Mode: {business_type}")
    print("Paste contact info (or 'done' to finish)")
    print("Format: email, name, company/neighborhood, city")
    print("Example: john@example.com, John Smith, ABC Properties, Raleigh\n")
    
    contacts = []
    
    while True:
        line = input("> ").strip()
        if line.lower() == 'done':
            break
        
        if not line:
            continue
        
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 4:
            print("❌ Need at least: email, name, company/neighborhood, city")
            continue
        
        email = parts[0]
        full_name = parts[1]
        company = parts[2]
        city = parts[3]
        
        # Split name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        contact = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'city': city
        }
        
        if business_type == 'homeowners':
            contact['neighborhood_name'] = company
            contact['street_name'] = ""
        elif business_type == 'property-managers':
            contact['company_name'] = company
            contact['property_name'] = ""
        elif business_type == 'hoa-contacts':
            contact['company_name'] = company
        else:  # real-estate-agents
            contact['company_name'] = company
        
        contacts.append(contact)
        print(f"✓ Added: {full_name} ({email})")
    
    if contacts:
        fieldnames = list(contacts[0].keys())
        append_to_csv(csv_file, contacts, fieldnames)
    
    return len(contacts)

def gather_leads_automated(business_type, max_per_city=10):
    """Automated lead gathering with rate limiting"""
    log_progress(f"🚀 Starting automated gathering for {business_type}")
    
    csv_file = TARGETS_DIR / f"{business_type}.csv"
    existing = load_existing_contacts(csv_file)
    
    total_found = 0
    
    for city in CITIES:
        queries = QUERIES.get(business_type, [])
        
        for query_template in queries:
            query = query_template.format(city)
            
            # Search and extract
            results = search_google_maps(query)
            
            # Filter out duplicates
            new_results = [r for r in results if r['email'].lower() not in existing]
            
            if new_results:
                # Determine fieldnames based on business type
                if business_type == 'property-managers':
                    fieldnames = ['email', 'first_name', 'last_name', 'company_name', 'property_name', 'city']
                elif business_type == 'hoa-contacts':
                    fieldnames = ['email', 'first_name', 'last_name', 'company_name', 'city']
                elif business_type == 'real-estate-agents':
                    fieldnames = ['email', 'first_name', 'last_name', 'company_name', 'city']
                else:  # homeowners
                    fieldnames = ['email', 'first_name', 'last_name', 'street_name', 'neighborhood_name', 'city']
                
                append_to_csv(csv_file, new_results, fieldnames)
                total_found += len(new_results)
                
                # Update existing set
                for r in new_results:
                    existing.add(r['email'].lower())
            
            # Rate limiting - random delay to appear more human
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            log_progress(f"⏳ Waiting {delay:.1f} seconds before next request...")
            time.sleep(delay)
            
            if total_found >= max_per_city:
                break
        
        if total_found >= max_per_city:
            break
    
    log_progress(f"✅ Gathering complete! Found {total_found} new contacts for {business_type}")
    return total_found

def main():
    """Main entry point"""
    print("🎯 Halo Pressure Washing - Lead Gathering Tool\n")
    print("Options:")
    print("1. Automated gathering (with rate limiting)")
    print("2. Manual entry mode (paste contacts)")
    print("3. Show current stats")
    
    choice = input("\nChoose (1-3): ").strip()
    
    if choice == '1':
        print("\nBusiness types:")
        print("1. Property Managers")
        print("2. HOA Contacts")
        print("3. Real Estate Agents")
        print("4. All of the above")
        
        type_choice = input("\nChoose (1-4): ").strip()
        
        types = {
            '1': ['property-managers'],
            '2': ['hoa-contacts'],
            '3': ['real-estate-agents'],
            '4': ['property-managers', 'hoa-contacts', 'real-estate-agents']
        }
        
        business_types = types.get(type_choice, [])
        max_per = int(input("Max leads per type (e.g., 50): ").strip() or "50")
        
        for btype in business_types:
            gather_leads_automated(btype, max_per_city=max_per)
    
    elif choice == '2':
        print("\nBusiness types:")
        print("1. Property Managers")
        print("2. HOA Contacts")
        print("3. Real Estate Agents")
        print("4. Homeowners")
        
        type_choice = input("\nChoose (1-4): ").strip()
        
        types = {
            '1': 'property-managers',
            '2': 'hoa-contacts',
            '3': 'real-estate-agents',
            '4': 'homeowners'
        }
        
        btype = types.get(type_choice)
        if btype:
            manual_entry_mode(btype)
    
    elif choice == '3':
        print("\n📊 Current Stats:\n")
        for csv_file in TARGETS_DIR.glob("*.csv"):
            if csv_file.name == 'README.md':
                continue
            
            count = 0
            if csv_file.exists():
                with open(csv_file, 'r') as f:
                    count = sum(1 for _ in f) - 1  # Subtract header
            
            print(f"{csv_file.stem}: {count} contacts")

if __name__ == "__main__":
    main()
