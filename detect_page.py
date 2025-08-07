from bs4 import BeautifulSoup

NO_RESULTS_AVAILABLE = "NO_RESULTS_AVAILABLE"
LIST_OF_ITEMS = "LIST_OF_ITEMS"
UNKNOWN = "UNKNOWN"

class NavigationModule:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def navigate(self):
        """Detects the current page type and returns a navigation status or item name."""
        html_content = self.driver.page_source
        page_type = self.detect_page_type(html_content)
        return self._map_page_type_to_status(page_type)

    def detect_page_type(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # No results
        if soup.find("div", class_="no-results-message"):
            return NO_RESULTS_AVAILABLE
        
        # List of items
        if soup.find("div", id="MainSearchTable_info", class_="dataTables_info"):
            return LIST_OF_ITEMS
        
        part_td = soup.find("td", attrs={"data-value": "Part Number"}, class_="sticky-col")
        if part_td:
            part_span = part_td.find("span", class_="part-number")
            if part_span and part_span.text.strip():
                return part_span.text.strip()

        return UNKNOWN

    def _map_page_type_to_status(self, page_type: str) -> str:
        """Maps detection results to the expected return values in your script."""
        if page_type == NO_RESULTS_AVAILABLE:
            return "NAVIGATION_FAILED"
        elif page_type == LIST_OF_ITEMS:
            return "LIST_OF_ITEMS"
        elif page_type == UNKNOWN:
            return "NAVIGATION_FAILED"
        else:
            # If a product name was returned, return it directly
            return page_type

