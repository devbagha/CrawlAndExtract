from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from google_search_scraper import GoogleSearchScraper
from email_scraper import EmailScraper
from save_to_csv import CSVWriter


def main():
    # Initialize WebDriver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    try:
        # Step 1: Search Google and collect URLs
        keyword = "Software companies usa"
        google_scraper = GoogleSearchScraper(driver, keyword)
        google_scraper.search_google()
        urls = google_scraper.extract_urls()

        print(f"Collected URLs: {len(urls)}")

        # Step 2: Visit URLs and scrape emails
        email_scraper = EmailScraper(driver)
        results = email_scraper.find_contact_page_and_emails(urls)

        # Step 3: Save the results to a CSV file
        CSVWriter.save_to_csv(results)

    finally:
        driver.quit()
        print("Process completed.")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
