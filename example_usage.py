#!/usr/bin/env python3
"""
Example script showing how to consume the Philippines holidays XML API
"""

import xml.etree.ElementTree as ET
import requests
from datetime import datetime

def load_holidays_from_url(url):
    """
    Load holidays from a remote XML URL
    """
    response = requests.get(url)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    return parse_holidays_xml(root)

def load_holidays_from_file(filename):
    """
    Load holidays from a local XML file
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    return parse_holidays_xml(root)

def parse_holidays_xml(root):
    """
    Parse holidays from XML root element
    """
    holidays = []
    
    for holiday in root.findall('holiday'):
        holiday_data = {
            'date': holiday.find('date').text,
            'day': holiday.find('day').text,
            'name': holiday.find('name').text,
            'mm_dd': holiday.find('mm_dd').text
        }
        holidays.append(holiday_data)
    
    return holidays

def find_holiday_by_date(holidays, target_date):
    """
    Find holiday by MM-DD format date
    """
    for holiday in holidays:
        if holiday['mm_dd'] == target_date:
            return holiday
    return None

def is_holiday_today(holidays):
    """
    Check if today is a holiday
    """
    today = datetime.now().strftime('%m-%d')
    return find_holiday_by_date(holidays, today)

def get_upcoming_holidays(holidays, days_ahead=30):
    """
    Get holidays coming up in the next N days
    """
    from datetime import datetime, timedelta
    
    today = datetime.now()
    upcoming = []
    
    for holiday in holidays:
        # Parse the MM-DD format and add current year
        month, day = map(int, holiday['mm_dd'].split('-'))
        holiday_date = datetime(today.year, month, day)
        
        # If the holiday has passed this year, check next year
        if holiday_date < today:
            holiday_date = datetime(today.year + 1, month, day)
        
        # Check if it's within the specified days ahead
        days_until = (holiday_date - today).days
        if 0 <= days_until <= days_ahead:
            upcoming.append({
                **holiday,
                'days_until': days_until,
                'full_date': holiday_date
            })
    
    # Sort by days until holiday
    upcoming.sort(key=lambda x: x['days_until'])
    return upcoming

def main():
    # Example 1: Load from local file
    print("=== Loading holidays from local file ===")
    try:
        holidays = load_holidays_from_file('ph_holidays.xml')
        print(f"Loaded {len(holidays)} holidays from local file")
    except FileNotFoundError:
        print("Local file not found, skipping...")
        holidays = []
    
    # Example 2: Load from remote URL (GitHub raw)
    print("\n=== Loading holidays from remote URL ===")
    try:
        # Replace with your actual GitHub repository URL
        url = "https://raw.githubusercontent.com/yourusername/ph-holidays-api/main/ph_holidays.xml"
        # For demo, we'll use the local file
        holidays = load_holidays_from_file('ph_holidays.xml')
        print(f"Loaded {len(holidays)} holidays from remote URL")
    except Exception as e:
        print(f"Failed to load from remote: {e}")
        return
    
    # Example 3: Check if today is a holiday
    print("\n=== Checking if today is a holiday ===")
    today_holiday = is_holiday_today(holidays)
    if today_holiday:
        print(f"🎉 Today is a holiday: {today_holiday['name']}")
    else:
        print("📅 Today is not a holiday")
    
    # Example 4: Find specific holiday
    print("\n=== Finding Christmas Day ===")
    christmas = find_holiday_by_date(holidays, '12-25')
    if christmas:
        print(f"🎄 {christmas['name']} is on {christmas['date']} ({christmas['day']})")
    
    # Example 5: Get upcoming holidays
    print("\n=== Upcoming holidays in the next 60 days ===")
    upcoming = get_upcoming_holidays(holidays, 60)
    for holiday in upcoming[:5]:  # Show first 5
        print(f"📅 {holiday['name']} - {holiday['date']} ({holiday['days_until']} days away)")
    
    # Example 6: List all holidays in MM-DD format
    print("\n=== All holidays in MM-DD format ===")
    for holiday in holidays:
        print(f"{holiday['mm_dd']} - {holiday['name']}")

if __name__ == "__main__":
    main()