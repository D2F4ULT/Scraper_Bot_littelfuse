from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from list_page_handler import click_first_result
from scrape_environmental_info import scrape_environmental_table
from detect_page import NavigationModule
from search_module import type_into_search
import time
from datasheet_scraper import extract_datasheet_link
from pprint import pprint
import csv  # ✅ Added
import os
from datetime import datetime

def create_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    # Set window size to 1920x1080
    opts.add_argument("window-size=1920,1080")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )


def scrape(driver):
    row_element = driver.find_element(By.CSS_SELECTOR, 'table tbody tr')  # Adjust selector as needed
    html = row_element.get_attribute('outerHTML')
    data = scrape_environmental_table(html)
    for key, value in data.items():
        print(f"{key}: {value}")

def read_part_numbers(csv_file):
    part_numbers = []
    rows = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            rows.append(row)
            if row and row[0].strip():
                part_numbers.append(row[0].strip())
    return part_numbers, header, rows

def write_remaining_parts(csv_file, header, rows, processed_part):
    """Rewrite the CSV without the processed_part row"""
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        for row in rows:
            if row and row[0].strip() != processed_part:
                writer.writerow(row)

def main():
    url = "https://www.littelfuse.com/"
    input_file = "input.csv"

    # Timestamped output filename:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output_{timestamp}.csv"

    FIELDNAMES = [
        'part_number', 'part_description', 'pb_free', 'rohs_date',
        'rohs_certificate_link', 'reach_status', 'reach_declaration_link',
        'ipc_material_declaration_link', 'halogen_free',
        'series', 'datasheet_link'  # NEW
    ]


    manual_mode = False   # <-- Set True for manual input (one part)
    modify_input = False   # <-- Set True to delete processed parts from input.csv

    if manual_mode:
        part_numbers = [input("Enter a part number to search for: ").strip()]
        header, rows = None, []
    else:
        part_numbers, header, rows = read_part_numbers(input_file)
        print(f"[INFO] Loaded {len(part_numbers)} part numbers from {input_file}")

    with open(output_file, mode='w', newline='', encoding='utf-8') as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=FIELDNAMES)
        writer.writeheader()

        for idx, part_or_keyword in enumerate(part_numbers):
            print(f"\n[INFO] Starting scrape for: {part_or_keyword}")
            driver = create_driver(headless=False)
            wait = WebDriverWait(driver, 10)

            try:
                driver.get(url)
                driver.set_window_size(1920, 1080)
                time.sleep(3)
                type_into_search(driver, part_or_keyword)
                time.sleep(3)

                nav_module = NavigationModule(driver, wait)
                result_type = nav_module.navigate()

                data = None

                if result_type == "LIST_OF_ITEMS":
                    click_first_result(driver, wait)
                    time.sleep(2)
                    try:
                        row_element = driver.find_element(By.CSS_SELECTOR, "table.envirnonmental-table tbody tr")
                        html = row_element.get_attribute("outerHTML")
                        full_html = driver.page_source
                        data = scrape_environmental_table(html, full_html)
                        pprint(data)
                    except Exception as e:
                        print("[ERROR] Couldn't locate environmental table row:", e)

                elif result_type == "NAVIGATION_FAILED":
                    print("[RESULT] No part found or unknown redirect.")

                else:
                    print(f"[RESULT] Landed on direct item page. Detected part: {result_type}")
                    if result_type.lower() != part_or_keyword.lower():
                        print(f"[SKIP] Detected part '{result_type}' does not match expected '{part_or_keyword}'. Skipping...")
                        data = None
                    else:
                        try:
                            row_element = driver.find_element(By.CSS_SELECTOR, "table.envirnonmental-table tbody tr")
                            html = row_element.get_attribute("outerHTML")
                            full_html = driver.page_source
                            data = scrape_environmental_table(html, full_html)

                            pprint(data)
                        except Exception as e:
                            print("[ERROR] Couldn't locate environmental table row:", e)
                            data = None

                row_to_write = {key: None for key in FIELDNAMES}
                row_to_write['part_number'] = part_or_keyword

                if data:
                    for key in FIELDNAMES:
                        row_to_write[key] = data.get(key, None)

                writer.writerow(row_to_write)

                # If modify_input is True and not manual_mode, remove processed part from input.csv
                if modify_input and not manual_mode:
                    print(f"[INFO] Removing processed part '{part_or_keyword}' from input CSV")
                    write_remaining_parts(input_file, header, rows, part_or_keyword)
                    # Also remove from rows list so next iteration is accurate
                    rows = [r for r in rows if r and r[0].strip() != part_or_keyword]

                time.sleep(5)

                if manual_mode:
                    print("[INFO] Manual mode: finished single scrape.")
                    break

            finally:
                driver.quit()
                print("[INFO] Browser closed.")
if __name__ == "__main__":
    main()
