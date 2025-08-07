from bs4 import BeautifulSoup

def scrape_environmental_table(html: str) -> dict:
    """Parse a table row and extract environmental info fields based on td[data-value]."""
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    # Loop over each <td> and check its data-value attribute
    for td in soup.find_all("td"):
        data_value = td.get("data-value", "").strip()

        if data_value == "Part Number":
            result["part_number"] = td.get_text(strip=True)

        elif data_value == "Part Description":
            result["part_description"] = td.get_text(strip=True)

        elif data_value == "RoHS":
            rohs_span = td.find("span", class_="desc")
            result["rohs_date"] = rohs_span.get_text(strip=True) if rohs_span else None

        elif data_value == "RoHS (2015/863/EU) Certificate":
            link = td.find("a", class_="link")
            result["rohs_certificate_link"] = link["href"] if link else None

        elif data_value == "REACH (SVHC's) Declaration":
            link = td.find("a", class_="link")
            result["reach_declaration_link"] = link["href"] if link else None

        elif data_value == "REACH (SVHC's)":
            result["reach_status"] = td.get_text(strip=True)

        elif data_value == "IPC-Material Declaration":
            link = td.find("a", class_="link")
            result["ipc_material_declaration_link"] = link["href"] if link else None

        elif data_value == "Pb-Free":
            result["pb_free"] = td.get_text(strip=True)

        elif data_value == "Halogen Free":
            result["halogen_free"] = td.get_text(strip=True)

    return result

