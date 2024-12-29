import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor

class EmailScraper:
    def __init__(self, keyword, max_workers=10):
        self.keyword = keyword
        self.max_workers = max_workers
        self.all_urls = []
        self.results = []
        self.driver = None

    def initialize_driver(self):
        return webdriver.Chrome(ChromeDriverManager().install())

    def extract_emails(self, text):
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(email_pattern, text)

    def scrape_contact_page(self, url):
        driver = self.initialize_driver()
        result = {"url": url, "emails": []}

        try:
            driver.get(url)
            time.sleep(2)  # Wait for the page to load

            # Try to find a "Contact" page link
            try:
                contact_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Contact")
                contact_url = contact_link.get_attribute("href")
                print(f"Contact page found: {contact_url}")
                driver.get(contact_url)
                time.sleep(2)  # Wait for the page to load

                # Scrape emails from the contact page
                page_source = driver.page_source
                emails = self.extract_emails(page_source)
                result["emails"] = emails
            except NoSuchElementException:
                print(f"No Contact page link found for {url}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        finally:
            driver.quit()

        return result

    def perform_search(self):
        self.driver = self.initialize_driver()
        self.driver.get("https://www.google.com")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

        # Perform a search
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(self.keyword)
        search_box.send_keys(Keys.RETURN)

        # Extract URLs from the search results
        while True:
            time.sleep(5)
            results = self.driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
            print(f"Found {len(results)} results on this page.")

            for result in results:
                url = result.get_attribute("href")
                if url not in self.all_urls:
                    self.all_urls.append(url)

            # Check if the "Next" button is available and click it
            try:
                next_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "pnnext"))
                )
                next_button.click()
                time.sleep(2)  # Wait for the next page to load
            except Exception:
                print("No more pages available.")
                break

        self.driver.quit()

    def scrape_all_contacts(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            self.results = list(executor.map(self.scrape_contact_page, self.all_urls))

    def save_to_csv(self, filename="scraped_emails.csv"):
        data = []
        for result in self.results:
            data.append([result["url"], "; ".join(result["emails"]) if result["emails"] else "No emails found"])

        df = pd.DataFrame(data, columns=["Contact Page URL", "Emails"])
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def run(self):
        start_time = time.time()

        print("Performing Google search...")
        self.perform_search()

        print("Scraping contact pages...")
        self.scrape_all_contacts()

        print("Saving results...")
        self.save_to_csv()

        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    keyword = "Software companies usa"
    scraper = EmailScraper(keyword)
    scraper.run()
