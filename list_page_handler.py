# list_page_handler.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def click_first_result(driver, wait):
    """Clicks the first product in the list of search results."""
    try:
        print("[INFO] Waiting for first search result...")
        first_result = wait.until(
            EC.element_to_be_clickable((By.ID, "coveo_index0"))
        )
        print("[INFO] Clicking on the first search result...")
        first_result.click()
        return True
    except TimeoutException:
        print("[ERROR] First search result did not load in time.")
        return False

