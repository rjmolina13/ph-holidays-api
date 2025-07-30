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
import json
import base64

def setup_webdriver():
    """
    Setup Chrome WebDriver with advanced anti-Cloudflare options
    """
    print("Setting up advanced anti-Cloudflare WebDriver...")
    chrome_options = Options()
    
    # Advanced Chrome arguments for maximum stealth
    options_list = [
        '--headless=new',  # Use new headless mode
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--window-size=1920,1080',
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        '--disable-blink-features=AutomationControlled',
        '--disable-extensions',
        '--disable-plugins',
        '--disable-images',
        '--remote-debugging-port=9222',
        '--disable-web-security',
        '--disable-features=VizDisplayCompositor',
        '--ignore-certificate-errors',
        '--ignore-ssl-errors',
        '--ignore-certificate-errors-spki-list',
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-renderer-backgrounding',
        '--disable-client-side-phishing-detection',
        '--disable-crash-reporter',
        '--disable-oopr-debug-crash-dump',
        '--no-crash-upload',
        '--disable-low-res-tiling',
        '--disable-ipc-flooding-protection',
        '--disable-default-apps',
        '--disable-hang-monitor',
        '--disable-prompt-on-repost',
        '--disable-sync',
        '--disable-domain-reliability',
        '--disable-features=TranslateUI',
        '--disable-component-extensions-with-background-pages',
        '--disable-background-networking',
        '--disable-component-update',
        '--metrics-recording-only',
        '--no-first-run',
        '--safebrowsing-disable-auto-update',
        '--password-store=basic',
        '--use-mock-keychain'
    ]
    
    print(f"Adding {len(options_list)} Chrome options...")
    for option in options_list:
        chrome_options.add_argument(option)
        print(f"  Added: {option}")
    
    # Advanced experimental options for stealth
    prefs = {
        "profile.default_content_setting_values": {
            "images": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "media_stream": 2,
        },
        "profile.managed_default_content_settings": {
            "images": 2
        },
        "profile.default_content_settings": {
            "popups": 0
        }
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    print("Adding experimental options...")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)
    print("  Added: excludeSwitches, useAutomationExtension, and detach")
    
    try:
        print("Initializing Chrome WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        print("Chrome WebDriver initialized successfully")
        
        # Execute comprehensive undetected-chromedriver-style anti-detection scripts
        print("Executing undetected-chromedriver-style comprehensive anti-detection scripts...")
        
        # Primary webdriver property removal
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Comprehensive navigator properties override
        driver.execute_script("""
            // Enhanced plugins array with realistic plugin objects
            Object.defineProperty(navigator, 'plugins', {
                get: () => {
                    const plugins = [
                        {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
                        {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: ''},
                        {name: 'Native Client', filename: 'internal-nacl-plugin', description: ''},
                        {name: 'WebKit built-in PDF', filename: 'WebKit built-in PDF', description: 'Portable Document Format'}
                    ];
                    plugins.length = 4;
                    return plugins;
                }
            });
            
            // Enhanced languages with realistic locale data
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en', 'en-PH']
            });
            
            // Enhanced language property
            Object.defineProperty(navigator, 'language', {
                get: () => 'en-US'
            });
        """)
        
        # Enhanced Chrome runtime with realistic properties
        driver.execute_script("""
            window.chrome = {
                runtime: {
                    onConnect: null,
                    onMessage: null
                },
                app: {
                    isInstalled: false
                },
                csi: function() {},
                loadTimes: function() {
                    return {
                        requestTime: Date.now() / 1000,
                        startLoadTime: Date.now() / 1000,
                        commitLoadTime: Date.now() / 1000,
                        finishDocumentLoadTime: Date.now() / 1000,
                        finishLoadTime: Date.now() / 1000,
                        firstPaintTime: Date.now() / 1000,
                        firstPaintAfterLoadTime: 0,
                        navigationType: 'Other'
                    };
                }
            };
        """)
        
        # Enhanced permissions API override
        driver.execute_script("""
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => {
                const permissions = {
                    'notifications': 'default',
                    'geolocation': 'denied',
                    'camera': 'denied',
                    'microphone': 'denied'
                };
                const state = permissions[parameters.name] || 'granted';
                return Promise.resolve({ state: state });
            };
        """)
        
        # Advanced canvas fingerprinting protection
        driver.execute_script("""
            const getContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type) {
                if (type === '2d') {
                    const context = getContext.call(this, type);
                    const originalFillText = context.fillText;
                    const originalStrokeText = context.strokeText;
                    const originalToDataURL = this.toDataURL;
                    
                    context.fillText = function() {
                        // Add slight noise to prevent fingerprinting
                        const noise = Math.random() * 0.0001;
                        arguments[1] += noise;
                        arguments[2] += noise;
                        return originalFillText.apply(this, arguments);
                    };
                    
                    context.strokeText = function() {
                        const noise = Math.random() * 0.0001;
                        arguments[1] += noise;
                        arguments[2] += noise;
                        return originalStrokeText.apply(this, arguments);
                    };
                    
                    this.toDataURL = function() {
                        // Return consistent but slightly randomized data
                        const originalData = originalToDataURL.apply(this, arguments);
                        return originalData;
                    };
                    
                    return context;
                }
                return getContext.call(this, type);
            };
        """)
        
        # Enhanced WebGL fingerprinting protection
        driver.execute_script("""
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                // Vendor and renderer spoofing
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';
                }
                // Max texture size
                if (parameter === 3379) {
                    return 16384;
                }
                // Max vertex attributes
                if (parameter === 34921) {
                    return 16;
                }
                // Shading language version
                if (parameter === 35724) {
                    return 'WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)';
                }
                return getParameter.call(this, parameter);
            };
            
            // Also patch WebGL2 if available
            if (window.WebGL2RenderingContext) {
                const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
                WebGL2RenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) return 'Intel Inc.';
                    if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                    return getParameter2.call(this, parameter);
                };
            }
        """)
        
        # Enhanced screen properties with realistic values
        driver.execute_script("""
            Object.defineProperty(screen, 'width', {get: () => 1920});
            Object.defineProperty(screen, 'height', {get: () => 1080});
            Object.defineProperty(screen, 'availWidth', {get: () => 1920});
            Object.defineProperty(screen, 'availHeight', {get: () => 1040});
            Object.defineProperty(screen, 'colorDepth', {get: () => 24});
            Object.defineProperty(screen, 'pixelDepth', {get: () => 24});
            Object.defineProperty(screen, 'orientation', {
                get: () => ({
                    angle: 0,
                    type: 'landscape-primary'
                })
            });
        """)
        
        # Additional undetected-chromedriver techniques
        driver.execute_script("""
            // Remove automation indicators
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
            
            // Override toString methods to hide automation
            const originalToString = Function.prototype.toString;
            Function.prototype.toString = function() {
                if (this === navigator.webdriver) {
                    return 'function webdriver() { [native code] }';
                }
                return originalToString.call(this);
            };
            
            // Mock realistic user agent data
            if (navigator.userAgentData) {
                Object.defineProperty(navigator, 'userAgentData', {
                    get: () => ({
                        brands: [
                            {brand: 'Google Chrome', version: '131'},
                            {brand: 'Chromium', version: '131'},
                            {brand: 'Not_A Brand', version: '24'}
                        ],
                        mobile: false,
                        platform: 'Windows'
                    })
                });
            }
            
            // Mock realistic connection info
            Object.defineProperty(navigator, 'connection', {
                get: () => ({
                    effectiveType: '4g',
                    rtt: 50,
                    downlink: 10,
                    saveData: false
                })
            });
            
            // Mock realistic memory info
            if (performance.memory) {
                Object.defineProperty(performance, 'memory', {
                    get: () => ({
                        usedJSHeapSize: 10000000 + Math.random() * 5000000,
                        totalJSHeapSize: 20000000 + Math.random() * 10000000,
                        jsHeapSizeLimit: 2172649472
                    })
                });
            }
        """)
        
        print("Undetected-chromedriver-style anti-detection scripts executed successfully")
        
        return driver
    except Exception as e:
        print(f"Error setting up Chrome WebDriver: {e}")
        print(f"Exception type: {type(e).__name__}")
        return None

def scrape_holidays(url):
    """
    Scrape holidays from the given URL using advanced anti-Cloudflare Selenium WebDriver
    """
    print(f"\n=== Starting advanced anti-Cloudflare holiday scraping process ===")
    print(f"Target URL: {url}")
    
    driver = setup_webdriver()
    if not driver:
        print("❌ Failed to setup WebDriver")
        return []
    
    try:
        print("\n📄 Loading page with advanced anti-Cloudflare WebDriver...")
        
        # Enhanced random delay with human-like patterns
        delay = random.uniform(3, 7)
        print(f"⏱️  Adding human-like delay: {delay:.1f} seconds before request...")
        time.sleep(delay)
        
        # Load the page
        print(f"🌐 Navigating to: {url}")
        start_time = time.time()
        driver.get(url)
        load_time = time.time() - start_time
        print(f"✅ Page navigation completed in {load_time:.2f} seconds")
        
        # Simulate human-like behavior immediately after page load
        print("🤖 Simulating human-like behavior...")
        driver.execute_script("""
            // Simulate realistic mouse movements
            const simulateMouseMovement = () => {
                for (let i = 0; i < 5; i++) {
                    const event = new MouseEvent('mousemove', {
                        clientX: Math.random() * window.innerWidth,
                        clientY: Math.random() * window.innerHeight,
                        bubbles: true
                    });
                    document.dispatchEvent(event);
                }
            };
            
            // Simulate scroll behavior
            const simulateScroll = () => {
                window.scrollTo({
                    top: Math.random() * 300,
                    behavior: 'smooth'
                });
            };
            
            // Simulate focus events
            const simulateFocus = () => {
                window.focus();
                document.body.focus();
            };
            
            // Execute simulations
            simulateMouseMovement();
            setTimeout(simulateScroll, 500);
            setTimeout(simulateFocus, 1000);
            
            // Trigger resize event
            setTimeout(() => {
                window.dispatchEvent(new Event('resize'));
            }, 1500);
        """)
        
        # Random post-load delay
        post_load_delay = random.uniform(2, 4)
        print(f"⏱️  Post-load human simulation delay: {post_load_delay:.1f} seconds")
        time.sleep(post_load_delay)
        
        # Enhanced Cloudflare detection and bypass
        print("\n🛡️  Enhanced Cloudflare protection detection...")
        page_title = driver.title
        page_source_snippet = driver.page_source[:2000].lower()
        print(f"📄 Initial page title: {page_title}")
        
        # Comprehensive Cloudflare indicators
        cloudflare_indicators = [
            "just a moment", "checking your browser", "cloudflare", "ddos protection",
            "ray id", "cf-ray", "attention required", "security check", "browser check",
            "please wait", "verifying you are human", "challenge"
        ]
        
        cloudflare_detected = any(
            indicator in page_title.lower() or indicator in page_source_snippet 
            for indicator in cloudflare_indicators
        )
        
        if cloudflare_detected:
            print("⚠️  Advanced Cloudflare protection detected, implementing sophisticated bypass...")
            print("🔧 Executing enhanced anti-detection scripts...")
            
            # Execute comprehensive anti-detection measures
            driver.execute_script("""
                // Enhanced timezone spoofing
                Date.prototype.getTimezoneOffset = function() {
                    return -480; // UTC+8 (Philippines timezone)
                };
                
                // Enhanced Intl API spoofing
                if (window.Intl && window.Intl.DateTimeFormat) {
                    const originalResolvedOptions = Intl.DateTimeFormat.prototype.resolvedOptions;
                    Intl.DateTimeFormat.prototype.resolvedOptions = function() {
                        const options = originalResolvedOptions.call(this);
                        options.timeZone = 'Asia/Manila';
                        options.locale = 'en-PH';
                        return options;
                    };
                }
                
                // Mock battery API with realistic values
                if (navigator.getBattery) {
                    navigator.getBattery = function() {
                        return Promise.resolve({
                            charging: Math.random() > 0.5,
                            chargingTime: Math.random() * 3600,
                            dischargingTime: Math.random() * 28800,
                            level: 0.3 + Math.random() * 0.7
                        });
                    };
                }
                
                // Enhanced connection API
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        rtt: 50 + Math.random() * 100,
                        downlink: 5 + Math.random() * 15,
                        saveData: false
                    })
                });
                
                // Mock hardware concurrency
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => 4 + Math.floor(Math.random() * 4)
                });
                
                // Enhanced memory spoofing
                if (navigator.deviceMemory) {
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => 4 + Math.floor(Math.random() * 4)
                    });
                }
                
                // Mock media devices
                if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
                    const originalEnumerate = navigator.mediaDevices.enumerateDevices;
                    navigator.mediaDevices.enumerateDevices = function() {
                        return Promise.resolve([
                            {deviceId: 'default', kind: 'audioinput', label: 'Default - Microphone'},
                            {deviceId: 'default', kind: 'audiooutput', label: 'Default - Speaker'},
                            {deviceId: 'default', kind: 'videoinput', label: 'Default - Camera'}
                        ]);
                    };
                }
            """)
            
            # Implement sophisticated waiting strategy with multiple attempts
            for attempt in range(4):
                wait_time = random.uniform(12, 25)
                print(f"🔄 Cloudflare bypass attempt {attempt + 1}/4: waiting {wait_time:.1f} seconds...")
                
                # Simulate realistic human behavior during wait
                for i in range(int(wait_time)):
                    time.sleep(1)
                    if i % 3 == 0:  # Every 3 seconds, simulate activity
                        driver.execute_script("""
                            // Random mouse movements
                            const event = new MouseEvent('mousemove', {
                                clientX: Math.random() * window.innerWidth,
                                clientY: Math.random() * window.innerHeight
                            });
                            document.dispatchEvent(event);
                            
                            // Occasional scroll
                            if (Math.random() > 0.7) {
                                window.scrollBy(0, Math.random() * 100 - 50);
                            }
                        """)
                
                # Check if challenge is completed
                current_title = driver.title
                current_source = driver.page_source[:2000].lower()
                
                challenge_completed = not any(
                    indicator in current_title.lower() or indicator in current_source 
                    for indicator in cloudflare_indicators
                )
                
                if challenge_completed:
                    print(f"✅ Cloudflare challenge bypassed successfully on attempt {attempt + 1}!")
                    print(f"📄 New page title: {current_title}")
                    break
                    
                # Additional human simulation between attempts
                driver.execute_script("""
                    // Simulate typing behavior
                    const keyEvent = new KeyboardEvent('keydown', {
                        key: 'Tab',
                        code: 'Tab',
                        bubbles: true
                    });
                    document.dispatchEvent(keyEvent);
                    
                    // Simulate window focus
                    window.focus();
                    
                    // Random click simulation
                    const clickEvent = new MouseEvent('click', {
                        clientX: window.innerWidth / 2,
                        clientY: window.innerHeight / 2,
                        bubbles: true
                    });
                    document.body.dispatchEvent(clickEvent);
                """)
            else:
                print("⚠️  Warning: Cloudflare challenge may not have completed after all attempts")
        
        # Enhanced page loading detection
        print("\n🔍 Enhanced page elements loading detection...")
        wait = WebDriverWait(driver, 60)  # Increased timeout
        
        try:
            print("  Searching for table with class 'publicholidays'...")
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "publicholidays")))
            print("  ✅ Found 'publicholidays' table!")
        except TimeoutException:
            print("  ⚠️  'publicholidays' table not found, trying enhanced fallback...")
            try:
                print("  Searching for any table element...")
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
                print("  ✅ Found table element (fallback)")
            except TimeoutException:
                print("  ⚠️  No table found, trying final enhanced fallback...")
                print("  Waiting for page body to load...")
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                print("  ✅ Page body loaded (final fallback)")
                
                # Enhanced dynamic content wait
                dynamic_wait = random.uniform(8, 15)
                print(f"  ⏱️  Enhanced dynamic content wait: {dynamic_wait:.1f} seconds...")
                time.sleep(dynamic_wait)
        
        # Final human simulation before extraction
        print("🎭 Final human behavior simulation...")
        driver.execute_script("""
            // Final comprehensive simulation
            window.focus();
            document.body.focus();
            
            // Simulate reading behavior (scroll down and up)
            window.scrollTo({top: document.body.scrollHeight / 2, behavior: 'smooth'});
            setTimeout(() => {
                window.scrollTo({top: 0, behavior: 'smooth'});
            }, 1000);
            
            // Final mouse movement
            const finalEvent = new MouseEvent('mousemove', {
                clientX: window.innerWidth / 2,
                clientY: window.innerHeight / 2
            });
            document.dispatchEvent(finalEvent);
        """)
        
        # Small delay after final simulation
        time.sleep(2)
        
        print("\n📋 Successfully loaded page with advanced anti-Cloudflare WebDriver!")
        
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
        try:
            driver.quit()
            print("✅ WebDriver closed successfully")
        except Exception as e:
            print(f"⚠️  Error closing WebDriver: {e}")
    
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