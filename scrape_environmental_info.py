# scrape_environmental_table.py
# ------------------------------
# This module is responsible for parsing the environmental table from a product's HTML page.
# It extracts various product-related details (e.g., RoHS status, Pb-free status, certificates)
# and can optionally also extract extra details such as the product series and datasheet link
# if the full HTML source of the page is provided.

from bs4 import BeautifulSoup  # Library for parsing HTML

def scrape_environmental_table(html: str, full_html: str = "") -> dict:
    """
    Parse environmental table and optionally extract 'series' and 'datasheet_link'.

    Args:
        html (str): HTML snippet containing the environmental table for the product.
        full_html (str, optional): Full HTML source of the product page, used to
                                   extract extra details. Defaults to an empty string.

    Returns:
        dict: A dictionary containing product and environmental attributes.
    """

    # Parse the provided HTML snippet into a BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    # Parse the full HTML (if provided) into a separate BeautifulSoup object
    full_soup = BeautifulSoup(full_html, "html.parser") if full_html else None

    # This dictionary will hold all extracted results
    result = {}

    # Iterate through all table cell elements <td> in the environmental info table
    for td in soup.find_all("td"):
        # The "data-value" attribute tells us which field this table cell represents
        data_value = td.get("data-value", "").strip()

        # --- Product details ---
        if data_value == "Part Number":
            result["part_number"] = td.get_text(strip=True)

        elif data_value == "Part Description":
            result["part_description"] = td.get_text(strip=True)

        # --- RoHS details ---
        elif data_value == "RoHS":
            rohs_span = td.find("span", class_="desc")
            # Extract the RoHS date if available
            result["rohs_date"] = rohs_span.get_text(strip=True) if rohs_span else None

        elif data_value == "RoHS (2015/863/EU) Certificate":
            link = td.find("a", class_="link")
            result["rohs_certificate_link"] = link["href"] if link else None

        # --- REACH details ---
        elif data_value == "REACH (SVHC's) Declaration":
            link = td.find("a", class_="link")
            result["reach_declaration_link"] = link["href"] if link else None

        elif data_value == "REACH (SVHC's)":
            result["reach_status"] = td.get_text(strip=True)

        # --- IPC Material Declaration ---
        elif data_value == "IPC-Material Declaration":
            link = td.find("a", class_="link")
            result["ipc_material_declaration_link"] = link["href"] if link else None

        # --- Pb-free & Halogen-free info ---
        elif data_value == "Pb-Free":
            result["pb_free"] = td.get_text(strip=True)

        elif data_value == "Halogen Free":
            result["halogen_free"] = td.get_text(strip=True)

    # If the full HTML page was provided, we can extract extra details
    if full_soup:
        # --- Series name ---
        series_span = full_soup.find("span", class_="series-short-desc")
        if series_span:
            text = series_span.get_text(strip=True)
            # Ensure the text contains "Series:" before extracting
            if "Series:" in text:
                result["series"] = text.split("Series:")[-1].strip()

        # --- Datasheet link ---
        datasheet_link = full_soup.find("a", class_="side-link datasheet-link")
        if datasheet_link and datasheet_link.get("href"):
            result["datasheet_link"] = datasheet_link["href"]

    # Return the compiled dictionary of results
    return result
