# datasheet_scraper.py

from bs4 import BeautifulSoup

def extract_datasheet_link(html: str) -> str:
    """
    Extract the datasheet link from the full product page HTML.
    
    Args:
        html (str): The full HTML source of the product page.
    
    Returns:
        str: The URL to the datasheet, or None if not found.
    """
    soup = BeautifulSoup(html, "html.parser")
    datasheet_a = soup.find("a", class_="datasheet-link")

    if datasheet_a and datasheet_a.has_attr("href"):
        return datasheet_a["href"]

    return None

