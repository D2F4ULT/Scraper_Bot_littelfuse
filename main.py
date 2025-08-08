from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Custom helper modules
from list_page_handler import click_first_result           # Handles clicking the first result in a list page
from scrape_environmental_info import scrape_environmental_table  # Parses environmental info table HTML
from detect_page import NavigationModule                   # Detects what type of page we've landed on
from search_module import type_into_search                 # Handles typing search terms into search bar
from datasheet_scraper import extract_datasheet_link       # Extracts datasheet link from page

import time
from pprint import pprint
import csv
import os
from datetime import datetime

# ------------------------------
# Create Chrome WebDriver
# ------------------------------
def create_driver(headless=True):
    """
    Creates and returns a configured Chrome WebDriver instance.
    :param headless: If True, runs browser in headless mode (no GUI).
    """
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")  # Use latest headless mode
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    # Set browser window size
    opts.add_argument("window-size=1920,1080")

    # Use ChromeDriverManager to automatically handle driver installation
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )

# ------------------------------
# Scrape one table row
# ------------------------------
def scrape(driver):
    """
    Scrapes the first environmental table row on the current page.
    """
    row_element = driver.find_element(By.CSS_SELECTOR, 'table tbody tr')  # Adjust selector as needed
    html = row_element.get_attribute('outerHTML')  # Get row HTML
    data = scrape_environmental_table(html)        # Parse environmental table row
    for key, value in data.items():
        print(f"{key}: {value}")

# ------------------------------
# Read part numbers from CSV
# ------------------------------
def read_part_numbers(csv_file):
    """
    Reads part numbers from a CSV file.
    Returns:
      - list of part numbers
      - header row
      - all rows from the file
    """
    part_numbers = []
    rows = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # Read header
        for row in reader:
            rows.append(row)
            if row and row[0].strip():
                part_numbers.append(row[0].strip())  # Use first column as part number
    return part_numbers, header, rows

# ------------------------------
# Remove processed part from CSV
# ------------------------------
def write_remaining_parts(csv_file, header, rows, processed_part):
    """
    Rewrites the CSV without the processed_part row.
    Useful if we want to remove parts we've already processed.
    """
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        for row in rows:
            if row and row[0].strip() != processed_part:
                writer.writerow(row)

# ------------------------------
# Main scraper logic
# ------------------------------
def main():
    url = "https://www.littelfuse.com/"
    input_file = "input.csv"

    # Create timestamped output filename (so each run is separate)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output_{timestamp}.csv"

    # Output CSV fields
    FIELDNAMES = [
        'part_number', 'part_description', 'pb_free', 'rohs_date',
        'rohs_certificate_link', 'reach_status', 'reach_declaration_link',
        'ipc_material_declaration_link', 'halogen_free',
        'series', 'datasheet_link'  # NEW field
    ]

    # Modes
    manual_mode = False   # If True → prompt for a single part number instead of reading from CSV
    modify_input = False  # If True → remove processed parts from input.csv

    # ------------------------------
    # Get part numbers
    # ------------------------------
    if manual_mode:
        # Manual input for single search
        part_numbers = [input("Enter a part number to search for: ").strip()]
        header, rows = None, []
    else:
        # Load part numbers from input.csv
        part_numbers, header, rows = read_part_numbers(input_file)
        print(f"[INFO] Loaded {len(part_numbers)} part numbers from {input_file}")

    # ------------------------------
    # Open output CSV for writing
    # ------------------------------
    with open(output_file, mode='w', newline='', encoding='utf-8') as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=FIELDNAMES)
        writer.writeheader()  # Write column headers

        # ------------------------------
        # Iterate over all part numbers
        # ------------------------------
        for idx, part_or_keyword in enumerate(part_numbers):
            print(f"\n[INFO] Starting scrape for: {part_or_keyword}")
            driver = create_driver(headless=False)  # Browser visible for debugging
            wait = WebDriverWait(driver, 10)  # Max wait time for elements

            try:
                # Load homepage
                driver.get(url)
                driver.set_window_size(1920, 1080)
                time.sleep(3)  # Small pause to allow page load

                # Search for the part number
                type_into_search(driver, part_or_keyword)
                time.sleep(3)

                # Detect where we landed after search
                nav_module = NavigationModule(driver, wait)
                result_type = nav_module.navigate()

                data = None  # Will hold scraped data

                # ------------------------------
                # If we landed on a list page
                # ------------------------------
                if result_type == "LIST_OF_ITEMS":
                    click_first_result(driver, wait)
                    time.sleep(2)
                    try:
                        # Locate environmental table row and scrape it
                        row_element = driver.find_element(By.CSS_SELECTOR, "table.envirnonmental-table tbody tr")
                        html = row_element.get_attribute("outerHTML")
                        full_html = driver.page_source
                        data = scrape_environmental_table(html, full_html)
                        pprint(data)
                    except Exception as e:
                        print("[ERROR] Couldn't locate environmental table row:", e)

                # ------------------------------
                # If navigation failed
                # ------------------------------
                elif result_type == "NAVIGATION_FAILED":
                    print("[RESULT] No part found or unknown redirect.")

                # ------------------------------
                # If we landed directly on an item page
                # ------------------------------
                else:
                    print(f"[RESULT] Landed on direct item page. Detected part: {result_type}")
                    if result_type.lower() != part_or_keyword.lower():
                        # Skip if detected part number doesn't match expected
                        print(f"[SKIP] Detected part '{result_type}' does not match expected '{part_or_keyword}'. Skipping...")
                        data = None
                    else:
                        try:
                            # Scrape environmental table
                            row_element = driver.find_element(By.CSS_SELECTOR, "table.envirnonmental-table tbody tr")
                            html = row_element.get_attribute("outerHTML")
                            full_html = driver.page_source
                            data = scrape_environmental_table(html, full_html)
                            pprint(data)
                        except Exception as e:
                            print("[ERROR] Couldn't locate environmental table row:", e)
                            data = None

                # ------------------------------
                # Prepare row for output CSV
                # ------------------------------
                row_to_write = {key: None for key in FIELDNAMES}  # Default None for all fields
                row_to_write['part_number'] = part_or_keyword

                if data:
                    for key in FIELDNAMES:
                        row_to_write[key] = data.get(key, None)

                writer.writerow(row_to_write)  # Save row to output CSV

                # ------------------------------
                # Remove processed part from input.csv if enabled
                # ------------------------------
                if modify_input and not manual_mode:
                    print(f"[INFO] Removing processed part '{part_or_keyword}' from input CSV")
                    write_remaining_parts(input_file, header, rows, part_or_keyword)
                    # Update local rows list
                    rows = [r for r in rows if r and r[0].strip() != part_or_keyword]

                time.sleep(5)  # Small delay to avoid hitting server too fast

                # ------------------------------
                # Manual mode → stop after one
                # ------------------------------
                if manual_mode:
                    print("[INFO] Manual mode: finished single scrape.")
                    break

            finally:
                # Always close browser, even if error occurs
                driver.quit()
                print("[INFO] Browser closed.")

# ------------------------------
# Script entry point
# ------------------------------
if __name__ == "__main__":
    main()
