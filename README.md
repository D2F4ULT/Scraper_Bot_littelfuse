# Littelfuse Scraper Bot

A Selenium-based automated scraper for extracting Littelfuse product information, including environmental compliance data, datasheet links, and series details.

## Features

- Automated search on Littelfuse website
- Handles multiple page types: no results, list of items, or single product
- Extracts detailed environmental compliance information
- Captures product series and datasheet links
- Clicks and navigates automatically through search results

## Project Structure

```
.
├── datasheet_scraper.py       # Extracts datasheet link from product HTML
├── navigation_module.py       # Detects page type and navigation state
├── list_page_handler.py       # Handles click on first search result in list
├── search_module.py           # Types search term into Littelfuse search bar
├── environmental_scraper.py   # Parses environmental compliance table
├── main.py                    # Entry point script
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Littelfuse-Scraper.git
cd Littelfuse-Scraper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure you have a compatible **Chrome** browser and **ChromeDriver** installed.

## Usage

Run the bot with:

```bash
python main.py
```

You may configure search terms and scraping behavior in `main.py`.

## Example Output

```json
{
  "part_number": "ABC123",
  "part_description": "Fast-acting Fuse",
  "rohs_date": "2024-03-10",
  "rohs_certificate_link": "https://www.littelfuse.com/rohs_cert.pdf",
  "reach_declaration_link": "https://www.littelfuse.com/reach.pdf",
  "reach_status": "Compliant",
  "ipc_material_declaration_link": "https://www.littelfuse.com/ipc.pdf",
  "pb_free": "Yes",
  "halogen_free": "Yes",
  "series": "ABC Series",
  "datasheet_link": "https://www.littelfuse.com/datasheet.pdf"
}
```

## Troubleshooting

- **Element not found**: Increase Selenium `WebDriverWait` timeout.
- **Empty results**: Check if search term is valid on Littelfuse site.
- **ChromeDriver errors**: Ensure ChromeDriver version matches your Chrome browser.

## License

MIT License. See `LICENSE` for details.
