from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class GoogleSearchScraper:
    def __init__(self, driver, keyword):
        self.driver = driver
        self.keyword = keyword
        self.urls = []

    def search_google(self):
        # Open Google
        self.driver.get("https://www.google.com")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

        # Enter the search query
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(self.keyword)
        search_box.send_keys(Keys.RETURN)

    def extract_urls(self):
        while True:
            time.sleep(5)
            # Extract URLs from the current page
            results = self.driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
            for result in results:
                url = result.get_attribute("href")
                if url not in self.urls:
                    self.urls.append(url)

            # Check if the "Next" button is available
            try:
                next_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "pnnext"))
                )
                next_button.click()
                time.sleep(2)  # Wait for the next page to load
            except Exception:
                print("No more pages available.")
                break

        return self.urls
