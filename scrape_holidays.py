#!/usr/bin/env python3
"""
Philippines Public Holidays Scraper
Scrapes holiday data from publicholidays.ph and converts to MM-DD format
"""

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import sys
import os
import time
import random

def scrape_holidays(url):
    """
    Scrape holidays from the given URL with enhanced anti-detection
    """
    try:
        # Create a session for better connection handling
        session = requests.Session()
        
        # Randomize user agents to avoid detection
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        
        # Enhanced headers to mimic real browser behavior
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        session.headers.update(headers)
        
        # Add random delay to avoid being flagged as bot
        delay = random.uniform(1, 3)
        print(f"Waiting {delay:.1f} seconds before request...")
        time.sleep(delay)
        
        # Make the request with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = session.get(url, timeout=30)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Attempt {attempt + 1} failed, retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
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