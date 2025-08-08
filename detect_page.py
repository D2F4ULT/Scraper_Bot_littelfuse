from bs4 import BeautifulSoup  # HTML parser for inspecting page structure

# Constants representing different detected page states
NO_RESULTS_AVAILABLE = "NO_RESULTS_AVAILABLE"
LIST_OF_ITEMS = "LIST_OF_ITEMS"
UNKNOWN = "UNKNOWN"

class NavigationModule:
    def __init__(self, driver, wait):
        """
        Initialize the navigation module.

        Args:
            driver: Selenium WebDriver instance for interacting with the browser.
            wait: Selenium WebDriverWait instance for waiting on page elements.
        """
        self.driver = driver
        self.wait = wait

    def navigate(self):
        """
        Detects the current page type and returns a status string.

        This is the main entry point used by main.py to decide what to do next.
        It retrieves the current page HTML from the driver, determines what
        type of page it is, and maps that to the expected status codes.

        Returns:
            str: One of:
                 - "NAVIGATION_FAILED" if no results or page type unknown
                 - "LIST_OF_ITEMS" if multiple results found
                 - Detected part number string if on a direct product page
        """
        # Get the entire HTML content of the current page
        html_content = self.driver.page_source

        # Determine what type of page we are on
        page_type = self.detect_page_type(html_content)

        # Convert detected page type to the status format expected by main.py
        return self._map_page_type_to_status(page_type)

    def detect_page_type(self, html_content: str) -> str:
        """
        Inspects the HTML to detect the type of page.

        Args:
            html_content (str): Full HTML of the page.

        Returns:
            str: One of the constants NO_RESULTS_AVAILABLE, LIST_OF_ITEMS, UNKNOWN,
                 or the detected part number if on a direct product page.
        """
        # Parse the HTML into a BeautifulSoup object
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Case 1: "No results" message present
        if soup.find("div", class_="no-results-message"):
            return NO_RESULTS_AVAILABLE
        
        # Case 2: Page contains a table info section → list of items view
        if soup.find("div", id="MainSearchTable_info", class_="dataTables_info"):
            return LIST_OF_ITEMS
        
        # Case 3: Direct product page → check for "Part Number" field
        part_td = soup.find("td", attrs={"data-value": "Part Number"}, class_="sticky-col")
        if part_td:
            # Inside that cell, find the <span class="part-number"> and get text
            part_span = part_td.find("span", class_="part-number")
            if part_span and part_span.text.strip():
                return part_span.text.strip()  # Return the actual part number string

        # Case 4: Could not determine → unknown
        return UNKNOWN

    def _map_page_type_to_status(self, page_type: str) -> str:
        """
        Maps internal detection results to the exact return values used in main.py.

        Args:
            page_type (str): Result from detect_page_type().

        Returns:
            str: Either "NAVIGATION_FAILED", "LIST_OF_ITEMS", or the part number.
        """
        if page_type == NO_RESULTS_AVAILABLE:
            return "NAVIGATION_FAILED"
        elif page_type == LIST_OF_ITEMS:
            return "LIST_OF_ITEMS"
        elif page_type == UNKNOWN:
            return "NAVIGATION_FAILED"
        else:
            # If we have an actual part number, return it directly
            return page_type
