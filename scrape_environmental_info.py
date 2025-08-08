from bs4 import BeautifulSoup

def scrape_environmental_table(html: str, full_html: str = "") -> dict:
    """Parse environmental table and also extract 'series' and 'datasheet_link'."""
    soup = BeautifulSoup(html, "html.parser")
    full_soup = BeautifulSoup(full_html, "html.parser") if full_html else None

    result = {}

    # Environmental info from <td data-value>
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

    # ✅ Extract additional info from the full HTML page
    if full_soup:
        # --- Series ---
        series_span = full_soup.find("span", class_="series-short-desc")
        if series_span:
            text = series_span.get_text(strip=True)
            if "Series:" in text:
                result["series"] = text.split("Series:")[-1].strip()

        # --- Datasheet Link ---
        datasheet_link = full_soup.find("a", class_="side-link datasheet-link")
        if datasheet_link and datasheet_link.get("href"):
            result["datasheet_link"] = datasheet_link["href"]

    return result

