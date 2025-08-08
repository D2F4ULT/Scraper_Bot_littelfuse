# search_module.py
# ----------------
# This module automates interacting with the Littelfuse website's search bar
# using Selenium. It types a search query into the input field, submits it,
# and then clicks away to dismiss any popups or dropdowns that might appear.

import time
import random

# Selenium imports for browser automation
from selenium.webdriver.common.by import By                  # For locating elements
from selenium.webdriver.common.keys import Keys              # For sending keyboard input
from selenium.webdriver.common.action_chains import ActionChains  # For complex mouse/keyboard actions
from selenium.webdriver.support.ui import WebDriverWait      # For waiting until conditions are met
from selenium.webdriver.support import expected_conditions as EC  # Predefined wait conditions

def type_into_search(driver, text, timeout=10):
    """
    Click into the Littelfuse search input, clear any existing text,
    type the given search text, submit it, and then click away from the
    search bar to dismiss any dropdown menus.

    Args:
        driver (WebDriver): Selenium WebDriver instance controlling the browser.
        text (str): The search term to type into the search input field.
        timeout (int, optional): Maximum time to wait for the search input to appear. Default is 10 seconds.

    Behavior:
        1. Waits for the search input to be visible.
        2. Clicks into it and clears any pre-existing text.
        3. Types the provided search text character-by-character.
        4. Submits the search with ENTER.
        5. Waits briefly for results to load.
        6. Clicks away to a random position on the page to hide search suggestions.
    """
    try:
        # --- Step 1: Wait for the search input to appear ---
        search_input = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,  # CSS selector used here to target element by attribute
                '[data-testid="mega-menu-search-input"]'
            ))
        )

        # --- Step 2: Focus the input field ---
        search_input.click()
        time.sleep(0.2)  # Short pause to ensure field is active

        # --- Step 3: Clear existing text ---
        search_input.send_keys(Keys.CONTROL, 'a')  # Select all text
        search_input.send_keys(Keys.BACKSPACE)     # Delete selection

        # --- Step 4: Type search text ---
        for char in text:
            search_input.send_keys(char)
            time.sleep(0.05)  # Slight delay between keystrokes for realism

        # --- Step 5: Submit search ---
        search_input.send_keys(Keys.ENTER)
        print(f"[INFO] Typed and submitted: '{text}'")

        # --- Step 6: Wait for results ---
        # Currently using a fixed sleep; could be replaced with explicit wait for specific element
        time.sleep(3)

        # --- Step 7: Click away to dismiss dropdown ---
        actions = ActionChains(driver)

        # Random click offset values (currently fixed to always click same spot)
        x_offset = random.randint(100, 100)  # Horizontal position relative to body
        y_offset = random.randint(0, 0)      # Vertical position relative to body

        # Locate <body> and click at offset
        body = driver.find_element(By.TAG_NAME, "body")
        actions.move_to_element_with_offset(body, x_offset, y_offset).click().perform()

        print(f"[INFO] Clicked away at offset ({x_offset}, {y_offset})")

    except Exception as e:
        # Catch any error during the search process
        print(f"[ERROR] Failed in search interaction: {e}")
