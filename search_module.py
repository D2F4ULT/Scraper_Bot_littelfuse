# search_module.py

import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def type_into_search(driver, text, timeout=10):
    """
    Clicks into Littelfuse search input, clears existing text, types input,
    and clicks away randomly to dismiss search dropdown.
    """
    try:
        # Wait for the input to become visible
        search_input = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 
                '[data-testid="mega-menu-search-input"]'
            ))
        )

        # Click into input field
        search_input.click()
        time.sleep(0.2)

        # Select all + delete existing text
        search_input.send_keys(Keys.CONTROL, 'a')
        search_input.send_keys(Keys.BACKSPACE)

        # Type character-by-character
        for char in text:
            search_input.send_keys(char)
            time.sleep(0.05)

        search_input.send_keys(Keys.ENTER)
        print(f"[INFO] Typed and submitted: '{text}'")

        # Wait for page load or results - simple wait
        time.sleep(3)  # You can change this to wait for specific element later

        # Click away to random screen coordinates using ActionChains
        actions = ActionChains(driver)

        # Random offset values — feel free to tweak the range
        x_offset = random.randint(100, 100)
        y_offset = random.randint(0, 0)

        # Move to body and click at offset
        body = driver.find_element(By.TAG_NAME, "body")
        actions.move_to_element_with_offset(body, x_offset, y_offset).click().perform()

        print(f"[INFO] Clicked away at offset ({x_offset}, {y_offset})")

    except Exception as e:
        print(f"[ERROR] Failed in search interaction: {e}")

