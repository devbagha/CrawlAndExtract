import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from scraper import Scraper
from config import KEYWORD, MAX_PAGES, OUTPUT_FILE

def main():
    # Start timer
    start_time = time.time()

    # Initialize Scraper
    scraper = Scraper(keyword=KEYWORD, max_pages=MAX_PAGES)

    # Search Google and collect URLs
    scraper.search_google()

    # Use ThreadPoolExecutor to scrape pages in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(scraper.scrape_contact_page, scraper.all_urls))

    # Process results into a DataFrame
    data = []
    for result in results:
        data.append([result["url"], "; ".join(result["emails"]) if result["emails"] else "No emails found"])

    df = pd.DataFrame(data, columns=["Contact Page URL", "Emails"])

    # Save the DataFrame to a CSV file
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data saved to {OUTPUT_FILE}")

    # End timer
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
