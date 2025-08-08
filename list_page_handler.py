# list_page_handler.py
# --------------------
# This module contains a helper function to click the first product
# in the search results list when the current page shows multiple items.
# It uses Selenium's WebDriverWait to ensure the element is clickable
# before attempting to interact with it.

from selenium.webdriver.common.by import By  # For locating elements (e.g., By.ID, By.CLASS_NAME)
from selenium.webdriver.support.ui import WebDriverWait  # For waiting until elements meet conditions
from selenium.webdriver.support import expected_conditions as EC  # Predefined wait conditions
from selenium.common.exceptions import TimeoutException  # Raised when a wait exceeds its time limit

def click_first_result(driver, wait):
    """
    Clicks the first product in the list of search results.

    Args:
        driver: Selenium WebDriver instance controlling the browser.
        wait: Selenium WebDriverWait instance for waiting until elements are ready.

    Returns:
        bool: True if the first result was clicked successfully, False if it timed out.
    """
    try:
        print("[INFO] Waiting for first search result...")

        # Wait until the element with ID "coveo_index0" (the first search result)
        # is clickable — meaning it exists in the DOM and is interactable.
        first_result = wait.until(
            EC.element_to_be_clickable((By.ID, "coveo_index0"))
        )

        print("[INFO] Clicking on the first search result...")
        first_result.click()  # Simulate the click action on the element
        return True

    except TimeoutException:
        # Triggered if the wait time expires without finding the clickable element
        print("[ERROR] First search result did not load in time.")
        return False
