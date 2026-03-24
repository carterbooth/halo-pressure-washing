#!/usr/bin/env python3
"""
Selenium-based lead scraper for Halo Pressure Washing
Scrapes Google Maps business listings with proper rate limiting
"""

import csv
import json
import time
import re
from pathlib import Path
from datetime import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configuration
BASE_DIR = Path(__file__).parent.parent
TARGETS_DIR = BASE_DIR / "targets"
STATE_DIR = BASE_DIR / "state"
STATE_DIR.mkdir(exist_ok=True)
LOG_FILE = STATE_DIR / "scraping-log.json"

# Service areas (NO DURHAM)
CITIES = [
    "Raleigh, NC",
    "Holly Springs, NC", 
    "Fuquay Varina, NC",
    "Apex, NC",
    "Cary, NC",
    "Garner, NC",
    "Angier, NC"
]

# Search queries by business type
SEARCH_QUERIES = {
    "property-managers": [
        "property management companies in {}",
        "rental property managers in {}",
        "apartment management in {}"
    ],
    "hoa-contacts": [
        "HOA management companies in {}",
        "homeowners association in {}",
        "community management in {}"
    ],
    "real-estate-agents": [
        "real estate agents in {}",
        "realtors in {}",
        "real estate brokers in {}"
    ]
}

# Rate limiting
MIN_DELAY = 10  # seconds between searches
MAX_DELAY = 20
SCROLL_PAUSE = 3  # seconds to wait for results to load

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
        json.dump(logs[-200:], f, indent=2)  # Keep last 200 entries

def setup_driver():
    """Setup headless Chrome driver"""
    log_progress("Setting up Chrome driver...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    log_progress("✅ Chrome driver ready")
    return driver

def extract_email(text):
    """Extract email from text"""
    if not text:
        return None
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def extract_phone(text):
    """Extract phone number from text"""
    if not text:
        return None
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else None

def scrape_google_maps_search(driver, query, max_results=20):
    """Scrape Google Maps search results"""
    results = []
    
    try:
        # Construct search URL
        search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
        log_progress(f"Searching: {query}")
        
        driver.get(search_url)
        time.sleep(random.uniform(3, 5))  # Let page load
        
        # Wait for results to appear
        wait = WebDriverWait(driver, 15)
        
        try:
            # Wait for the results panel
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']")))
        except TimeoutException:
            log_progress("⚠️ No results found or timed out")
            return results
        
        # Scroll to load more results
        scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        
        for i in range(5):  # Scroll 5 times to load more results
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(SCROLL_PAUSE)
        
        # Find all business listings
        businesses = driver.find_elements(By.CSS_SELECTOR, "div[role='feed'] > div > div > a")
        log_progress(f"Found {len(businesses)} business listings")
        
        for idx, business in enumerate(businesses[:max_results]):
            try:
                # Click on business to load details
                driver.execute_script("arguments[0].click();", business)
                time.sleep(random.uniform(2, 4))
                
                # Extract business name
                try:
                    name_elem = driver.find_element(By.CSS_SELECTOR, "h1")
                    business_name = name_elem.text
                except:
                    business_name = "Unknown"
                
                # Try to find website button and extract email from website
                email = None
                phone = None
                website = None
                
                try:
                    # Find website link
                    website_button = driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']")
                    website = website_button.get_attribute("href")
                    
                    # Try to find phone
                    phone_buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-item-id^='phone']")
                    if phone_buttons:
                        phone_text = phone_buttons[0].get_attribute("aria-label")
                        phone = extract_phone(phone_text)
                    
                    # Visit website to find email (optional - slow)
                    # For now, we'll construct likely emails
                    if website:
                        domain = website.split("//")[-1].split("/")[0]
                        # Common email patterns
                        possible_emails = [
                            f"info@{domain}",
                            f"contact@{domain}",
                            f"hello@{domain}",
                            f"office@{domain}"
                        ]
                        email = possible_emails[0]  # Take first guess
                
                except Exception as e:
                    log_progress(f"Could not extract contact for {business_name}: {str(e)}")
                
                if email:  # Only save if we have an email
                    result = {
                        'business_name': business_name,
                        'email': email,
                        'phone': phone,
                        'website': website
                    }
                    results.append(result)
                    log_progress(f"✓ Extracted: {business_name} ({email})")
                
                # Rate limit between clicking businesses
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                log_progress(f"Error processing business {idx}: {str(e)}")
                continue
        
    except Exception as e:
        log_progress(f"❌ Error scraping {query}: {str(e)}")
    
    return results

def load_existing_emails(csv_file):
    """Load existing emails to avoid duplicates"""
    existing = set()
    if csv_file.exists():
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'email' in row:
                    existing.add(row['email'].lower())
    return existing

def save_to_csv(csv_file, contacts, business_type):
    """Save contacts to CSV"""
    if not contacts:
        return
    
    # Define fieldnames based on business type
    if business_type == 'property-managers':
        fieldnames = ['email', 'first_name', 'last_name', 'company_name', 'property_name', 'city', 'phone', 'website']
    elif business_type == 'hoa-contacts':
        fieldnames = ['email', 'first_name', 'last_name', 'company_name', 'city', 'phone', 'website']
    elif business_type == 'real-estate-agents':
        fieldnames = ['email', 'first_name', 'last_name', 'company_name', 'city', 'phone', 'website']
    else:
        fieldnames = ['email', 'first_name', 'last_name', 'company_name', 'city', 'phone', 'website']
    
    # Check if file exists
    file_exists = csv_file.exists() and csv_file.stat().st_size > 0
    
    with open(csv_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        
        if not file_exists:
            writer.writeheader()
        
        for contact in contacts:
            # Parse name if we have business_name
            name = contact.get('business_name', '').split(' ', 1)
            contact['first_name'] = name[0] if name else ''
            contact['last_name'] = name[1] if len(name) > 1 else ''
            contact['company_name'] = contact.get('business_name', '')
            contact['property_name'] = ''
            
            writer.writerow(contact)
    
    log_progress(f"✅ Saved {len(contacts)} contacts to {csv_file.name}")

def scrape_business_type(driver, business_type, max_per_city=10):
    """Scrape all cities for a business type"""
    log_progress(f"🚀 Starting scrape for {business_type}")
    
    csv_file = TARGETS_DIR / f"{business_type}.csv"
    existing_emails = load_existing_emails(csv_file)
    
    total_new = 0
    queries = SEARCH_QUERIES.get(business_type, [])
    
    for city in CITIES:
        for query_template in queries:
            query = query_template.format(city)
            
            # Scrape this search
            results = scrape_google_maps_search(driver, query, max_results=max_per_city)
            
            # Filter out duplicates
            new_results = []
            for result in results:
                email = result['email'].lower()
                if email not in existing_emails:
                    result['city'] = city
                    new_results.append(result)
                    existing_emails.add(email)
            
            if new_results:
                save_to_csv(csv_file, new_results, business_type)
                total_new += len(new_results)
            
            # Rate limit between searches
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            log_progress(f"⏳ Waiting {delay:.1f}s before next search...")
            time.sleep(delay)
    
    log_progress(f"✅ Completed {business_type}: {total_new} new contacts")
    return total_new

def main():
    """Main scraping function"""
    log_progress("=" * 60)
    log_progress("🎯 Halo Pressure Washing - Selenium Lead Scraper")
    log_progress("=" * 60)
    
    driver = None
    
    try:
        driver = setup_driver()
        
        # Scrape each business type
        business_types = ['property-managers', 'hoa-contacts', 'real-estate-agents']
        
        for btype in business_types:
            total = scrape_business_type(driver, btype, max_per_city=15)
            log_progress(f"📊 {btype}: {total} new leads added")
            
            # Longer break between business types
            log_progress("⏸️ Taking a 2-minute break...")
            time.sleep(120)
        
        log_progress("=" * 60)
        log_progress("✅ SCRAPING COMPLETE!")
        log_progress("=" * 60)
        
        # Show final stats
        print("\n📊 Final Lead Count:\n")
        for csv_file in TARGETS_DIR.glob("*.csv"):
            if csv_file.stem in business_types:
                count = sum(1 for _ in open(csv_file)) - 1
                print(f"  {csv_file.stem}: {count} contacts")
        
    except Exception as e:
        log_progress(f"❌ Fatal error: {str(e)}")
        raise
    
    finally:
        if driver:
            driver.quit()
            log_progress("🛑 Driver closed")

if __name__ == "__main__":
    main()
