#!/usr/bin/env python3
"""
Philippines Public Holidays Scraper
Scrapes holiday data from publicholidays.ph and converts to MM-DD format
"""

import os
import sys
import time
import random
from datetime import datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def setup_webdriver():
    """
    Setup Chrome WebDriver with headless options
    """
    print("Setting up Chrome WebDriver...")
    chrome_options = Options()
    
    # Add Chrome arguments with verbose logging
    options_list = [
        '--headless',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--window-size=1920,1080',
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        '--disable-blink-features=AutomationControlled',
        '--disable-extensions',
        '--disable-plugins',
        '--disable-images',
        '--remote-debugging-port=9222'
    ]
    
    print(f"Adding {len(options_list)} Chrome options...")
    for option in options_list:
        chrome_options.add_argument(option)
        print(f"  Added: {option}")
    
    print("Adding experimental options...")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    print("  Added: excludeSwitches and useAutomationExtension")
    
    try:
        print("Initializing Chrome WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        print("Chrome WebDriver initialized successfully")
        
        print("Executing anti-detection script...")
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("Anti-detection script executed")
        
        return driver
    except Exception as e:
        print(f"Error setting up Chrome WebDriver: {e}")
        print(f"Exception type: {type(e).__name__}")
        return None

def scrape_holidays(url):
    """
    Scrape holidays from the given URL using Selenium WebDriver
    """
    print(f"\n=== Starting holiday scraping process ===")
    print(f"Target URL: {url}")
    
    driver = setup_webdriver()
    if not driver:
        print("❌ Failed to setup WebDriver")
        return []
    
    try:
        print("\n📄 Loading page with WebDriver...")
        
        # Add random delay to avoid being flagged as bot
        delay = random.uniform(2, 4)
        print(f"⏱️  Waiting {delay:.1f} seconds before request...")
        time.sleep(delay)
        
        # Load the page
        print(f"🌐 Navigating to: {url}")
        start_time = time.time()
        driver.get(url)
        load_time = time.time() - start_time
        print(f"✅ Page navigation completed in {load_time:.2f} seconds")
        
        # Wait for the page to load completely with increased timeout
        print("\n🔍 Waiting for page elements to load...")
        wait = WebDriverWait(driver, 30)
        
        try:
            print("  Searching for table with class 'publicholidays'...")
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "publicholidays")))
            print("  ✅ Found 'publicholidays' table!")
        except TimeoutException:
            print("  ⚠️  'publicholidays' table not found, trying fallback...")
            try:
                print("  Searching for any table element...")
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
                print("  ✅ Found table element (fallback)")
            except TimeoutException:
                print("  ⚠️  No table found, trying final fallback...")
                print("  Waiting for page body to load...")
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                print("  ✅ Page body loaded (final fallback)")
                print("  ⏱️  Giving extra 5 seconds for dynamic content...")
                time.sleep(5)
        
        print("\n📋 Successfully loaded page with WebDriver!")
        
        # Get page source and parse with BeautifulSoup
        print("📄 Extracting page source...")
        page_source = driver.page_source
        page_size = len(page_source)
        print(f"✅ Page source extracted ({page_size:,} characters)")
        
    except TimeoutException as e:
        print(f"❌ Timeout waiting for page to load: {e}")
        return []
    except WebDriverException as e:
        print(f"❌ WebDriver error: {e}")
        print(f"Exception type: {type(e).__name__}")
        return []
    finally:
        print("🔄 Closing WebDriver...")
        driver.quit()
        print("✅ WebDriver closed")
    
    print("🍲 Parsing page content with BeautifulSoup...")
    soup = BeautifulSoup(page_source, 'html.parser')
    
    print("🔍 Looking for holidays table...")
    
    # Debug: Print page title and check for any tables
    title = soup.find('title')
    print(f"📄 Page title: {title.get_text() if title else 'No title found'}")
    
    all_tables = soup.find_all('table')
    print(f"📊 Found {len(all_tables)} table(s) on the page")
    
    for i, table in enumerate(all_tables):
        classes = table.get('class', [])
        print(f"  Table {i+1}: classes = {classes}")
        if classes:
            for cls in classes:
                print(f"    - {cls}")
    
    # Find the holidays table
    table = soup.find('table', class_='publicholidays')
    if not table:
        print("❌ Could not find holidays table with class 'publicholidays'")
        
        # Try alternative approaches
        print("🔍 Trying alternative table selection methods...")
        
        # Try finding table by content
        for i, alt_table in enumerate(all_tables):
            rows = alt_table.find_all('tr')
            if len(rows) > 5:  # Likely a data table
                print(f"  Checking table {i+1} with {len(rows)} rows...")
                first_row = rows[0] if rows else None
                if first_row:
                    cells = first_row.find_all(['th', 'td'])
                    cell_texts = [cell.get_text().strip() for cell in cells]
                    print(f"    First row cells: {cell_texts}")
                    
                    # Check if this looks like a holidays table
                    if any('date' in text.lower() or 'holiday' in text.lower() or 'day' in text.lower() for text in cell_texts):
                        print(f"    ✅ Table {i+1} looks like a holidays table, using it!")
                        table = alt_table
                        break
        
        if not table:
            return []
    
    print("✅ Found holidays table, extracting data...")
    holidays = []
    rows = table.find('tbody').find_all('tr')
    print(f"📊 Processing {len(rows)} table rows...")
    
    for i, row in enumerate(rows, 1):
        cells = row.find_all('td')
        if len(cells) >= 3 and not row.find('td', class_='adunit'):
            date_text = cells[0].get_text().strip()
            day_text = cells[1].get_text().strip()
            holiday_name = cells[2].get_text().strip()
            
            print(f"  Row {i}: Processing '{holiday_name}' on {date_text}")
            
            # Skip empty or invalid rows
            if not date_text or not holiday_name:
                print(f"    ⚠️  Skipping row {i}: empty date or name")
                continue
                
            # Parse date (format: "1 Jan", "25 Dec", etc.)
            try:
                # Add current year for parsing
                current_year = datetime.now().year
                date_with_year = f"{date_text} {current_year}"
                parsed_date = datetime.strptime(date_with_year, "%d %b %Y")
                
                # Convert to MM-DD format
                mm_dd_format = parsed_date.strftime("%m-%d")
                
                holidays.append({
                    'date': date_text,
                    'day': day_text,
                    'name': holiday_name,
                    'mm_dd': mm_dd_format
                })
                print(f"    ✅ Added holiday: {holiday_name} ({mm_dd_format})")
            except ValueError as e:
                print(f"    ❌ Warning: Could not parse date '{date_text}': {e}")
                continue
        else:
            print(f"  Row {i}: Skipping (insufficient cells or ad unit)")
    
    print(f"\n🎉 Successfully extracted {len(holidays)} holidays!")
    return holidays

def create_xml(holidays, output_file):
    """
    Create XML file with holiday data
    """
    root = ET.Element("holidays")
    root.set("year", str(datetime.now().year))
    root.set("country", "Philippines")
    root.set("last_updated", datetime.now().isoformat())
    
    for holiday in holidays:
        holiday_elem = ET.SubElement(root, "holiday")
        
        date_elem = ET.SubElement(holiday_elem, "date")
        date_elem.text = holiday['date']
        
        day_elem = ET.SubElement(holiday_elem, "day")
        day_elem.text = holiday['day']
        
        name_elem = ET.SubElement(holiday_elem, "name")
        name_elem.text = holiday['name']
        
        mm_dd_elem = ET.SubElement(holiday_elem, "mm_dd")
        mm_dd_elem.text = holiday['mm_dd']
    
    # Create the tree and write to file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    
    with open(output_file, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)
    
    print(f"XML file created: {output_file}")

def main():
    # Default URL - can be overridden by environment variable
    url = os.getenv('HOLIDAYS_URL', 'https://publicholidays.ph/2025-dates/')
    output_file = os.getenv('OUTPUT_FILE', 'ph_holidays.xml')
    
    print(f"Scraping holidays from: {url}")
    
    holidays = scrape_holidays(url)
    
    if not holidays:
        print("No holidays found!")
        sys.exit(1)
    
    print(f"Found {len(holidays)} holidays:")
    for holiday in holidays:
        print(f"  {holiday['mm_dd']} - {holiday['name']}")
    
    create_xml(holidays, output_file)
    print(f"Successfully created {output_file} with {len(holidays)} holidays")

if __name__ == "__main__":
    main()