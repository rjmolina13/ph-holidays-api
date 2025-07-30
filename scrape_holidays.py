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
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"Error setting up Chrome WebDriver: {e}")
        return None

def scrape_holidays(url):
    """
    Scrape holidays from the given URL using Selenium WebDriver
    """
    driver = setup_webdriver()
    if not driver:
        print("Failed to setup WebDriver")
        return []
    
    try:
        print("Loading page with WebDriver...")
        
        # Add random delay to avoid being flagged as bot
        delay = random.uniform(2, 4)
        print(f"Waiting {delay:.1f} seconds before request...")
        time.sleep(delay)
        
        # Load the page
        driver.get(url)
        
        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "publicholidays"))
        )
        
        print("Successfully loaded page with WebDriver!")
        
        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        
    except TimeoutException:
        print("Timeout waiting for page to load")
        return []
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
        return []
    finally:
        driver.quit()
    
    try:
        
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find the holidays table
        table = soup.find('table', class_='publicholidays')
        if not table:
            raise Exception("Could not find holidays table")
        
        holidays = []
        rows = table.find('tbody').find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3 and not row.find('td', class_='adunit'):
                date_text = cells[0].get_text().strip()
                day_text = cells[1].get_text().strip()
                holiday_name = cells[2].get_text().strip()
                
                # Skip empty or invalid rows
                if not date_text or not holiday_name:
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
                except ValueError as e:
                    print(f"Warning: Could not parse date '{date_text}': {e}")
                    continue
        
        return holidays
        
    except Exception as e:
        print(f"Error scraping holidays: {e}")
        return []

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