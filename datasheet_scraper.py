# datasheet_scraper.py
# ---------------------
# This module contains a helper function to extract a datasheet link
# from the HTML of a product page. It uses BeautifulSoup to parse the HTML
# and look for an anchor tag with a specific CSS class ("datasheet-link").

from bs4 import BeautifulSoup  # HTML parsing library

def extract_datasheet_link(html: str) -> str:
    """
    Extract the datasheet link from the full product page HTML.

    Args:
        html (str): The full HTML source of the product page as a string.

    Returns:
        str: The URL to the datasheet, or None if not found.
    """

    # Parse the HTML string into a BeautifulSoup object for easy querying
    soup = BeautifulSoup(html, "html.parser")

    # Search for the first <a> element with class="datasheet-link"
    datasheet_a = soup.find("a", class_="datasheet-link")

    # If such an element exists and it has an "href" attribute,
    # return the value of that attribute (the link URL)
    if datasheet_a and datasheet_a.has_attr("href"):
        return datasheet_a["href"]

    # If no matching link is found, return None
    return None
