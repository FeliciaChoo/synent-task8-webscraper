# synent-task8-webscraper-chooenyi
Automated Python Web Scraper using BeautifulSoup &amp; Requests
# Task 8: Automated Web Scraper (BeautifulSoup & Requests)

A Python web scraping tool built for the **Synent Technologies Python Development Internship Program**. It extracts structured product data across paginated catalog pages from *Books to Scrape* (`books.toscrape.com`) and exports cleaned datasets into both CSV and JSON formats.

## Features
- **Paginated Extraction:** Scrapes user-defined page ranges (up to 50 pages / 1,000 books) with polite request throttling (`time.sleep`).
- **Structured Data Cleaning:** Extracts book titles, numeric GBP prices, 1–5 star ratings, stock availability, and resolved product URLs.
- **Dual Format Export:** Automatically generates `output/books_data.csv` and `output/books_data.json`, plus displays summary statistics (total count and average price) in the terminal.

## Tech Stack
- Python 3
- `requests`
- `beautifulsoup4`
- Standard Library (`csv`, `json`, `pathlib`, `urllib.parse`)

## Setup & Usage
1. Clone the repository:
   ```bash
   git clone [https://github.com/](https://github.com/)<your-github-username>/synent-task8-webscraper-chooenyi.git
   cd synent-task8-webscraper-chooenyi
