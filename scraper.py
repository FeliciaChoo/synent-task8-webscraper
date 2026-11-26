import csv
import json
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/"
START_PAGE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PythonScraper/1.0"
}


def parse_book_card(article: BeautifulSoup) -> dict:
    """Extract structured details from a single book <article class='product_pod'> element."""
    title_tag = article.h3.a
    title = title_tag["title"].strip()
    relative_href = title_tag["href"]
    product_url = urljoin(BASE_URL, relative_href)

    raw_price = article.select_one("p.price_color").get_text(strip=True)
    # Clean currency encoding artifact (e.g., 'Â£51.77' -> 51.77)
    clean_price = float(raw_price.replace("Â", "").replace("£", "").strip())

    availability = article.select_one("p.instock.availability").get_text(strip=True)

    rating_classes = article.select_one("p.star-rating").get("class", [])
    rating_word = next((c for c in rating_classes if c in RATING_MAP), "Unknown")
    rating_num = RATING_MAP.get(rating_word, 0)

    return {
        "title": title,
        "price_gbp": clean_price,
        "rating": rating_num,
        "availability": availability,
        "url": product_url,
    }


def scrape_pages(max_pages: int = 3, delay: float = 0.5) -> list[dict]:
    """Scrape book records across multiple paginated catalog pages."""
    scraped_books = []

    for page in range(1, max_pages + 1):
        url = START_PAGE_URL.format(page)
        print(f"[Info] Scraping page {page}/{max_pages}: {url}")

        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 404:
            print(f"[Warn] Page {page} does not exist. Stopping pagination.")
            break
        response.raise_for_status()
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article.product_pod")

        for article in articles:
            scraped_books.append(parse_book_card(article))

        if page < max_pages:
            time.sleep(delay)

    return scraped_books


def save_to_csv(records: list[dict], filepath: Path) -> None:
    """Export scraped records to a UTF-8 CSV file."""
    if not records:
        return
    with filepath.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def save_to_json(records: list[dict], filepath: Path) -> None:
    """Export scraped records to a formatted JSON file."""
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def main() -> None:
    print("=== Synent Technologies | Automated Book Web Scraper ===")
    raw_input = input("How many pages to scrape? (Default = 3, Max = 50): ").strip()

    try:
        pages = int(raw_input) if raw_input else 3
        if pages < 1 or pages > 50:
            raise ValueError("Please enter a number between 1 and 50.")
    except ValueError as err:
        print(f"[Error] Invalid input: {err}")
        return

    try:
        books = scrape_pages(max_pages=pages)
        if not books:
            print("[Warn] No data extracted.")
            return

        output_dir = Path(__file__).resolve().parent / "output"
        output_dir.mkdir(exist_ok=True)

        csv_path = output_dir / "books_data.csv"
        json_path = output_dir / "books_data.json"

        save_to_csv(books, csv_path)
        save_to_json(books, json_path)

        avg_price = sum(b["price_gbp"] for b in books) / len(books)
        print("\n" + "=" * 48)
        print(f"  SCRAPING COMPLETE: {len(books)} books extracted")
        print(f"  Average Price : £{avg_price:.2f}")
        print(f"  CSV Saved To  : {csv_path}")
        print(f"  JSON Saved To : {json_path}")
        print("=" * 48)
        print("\nSample Record:")
        print(json.dumps(books[0], indent=2))

    except requests.exceptions.RequestException as err:
        print(f"[Network Error] Request failed: {err}")


if __name__ == "__main__":
    main()