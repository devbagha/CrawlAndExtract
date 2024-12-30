import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from driver_manager import initialize_driver
from utils import extract_emails

class Scraper:
    def __init__(self, keyword, max_pages=5):
        self.keyword = keyword
        self.max_pages = max_pages
        self.all_urls = []

    def search_google(self):
        """Perform a Google search and collect URLs."""
        driver = initialize_driver()
        try:
            driver.get("https://www.google.com")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(self.keyword)
            search_box.send_keys(Keys.RETURN)

            for page in range(self.max_pages):
                time.sleep(5)
                results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
                print(f"Found {len(results)} results on page {page + 1}.")

                for result in results:
                    url = result.get_attribute("href")
                    if url not in self.all_urls:
                        self.all_urls.append(url)

                try:
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "pnnext"))
                    )
                    next_button.click()
                    time.sleep(2)
                except Exception:
                    print("No more pages available.")
                    break
        finally:
            driver.quit()

    def scrape_contact_page(self, url):
        """Scrape emails from a contact page."""
        driver = initialize_driver()
        result = {"url": url, "emails": []}
        try:
            driver.get(url)
            time.sleep(2)
            try:
                contact_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Contact")
                contact_url = contact_link.get_attribute("href")
                print(f"Contact page found: {contact_url}")
                driver.get(contact_url)
                time.sleep(2)
                page_source = driver.page_source
                result["emails"] = extract_emails(page_source)
            except NoSuchElementException:
                print(f"No Contact page link found for {url}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        finally:
            driver.quit()
        return result
