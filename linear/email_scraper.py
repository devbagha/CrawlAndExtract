import re
import time
from selenium.webdriver.common.by import By


class EmailScraper:
    def __init__(self, driver):
        self.driver = driver
        self.results = {}

    @staticmethod
    def extract_emails(text):
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(email_pattern, text)

    def scrape_contact_page(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)
            page_source = self.driver.page_source
            emails = self.extract_emails(page_source)
            return emails
        except Exception:
            return []

    def find_contact_page_and_emails(self, urls):
        for url in urls:
            try:
                print(f"Visiting: {url}")
                self.driver.get(url)
                time.sleep(2)
                
                # Try to find a "Contact" page link
                try:
                    contact_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Contact")
                    contact_url = contact_link.get_attribute("href")
                    print(f"Contact page found: {contact_url}")
                except:
                    print(f"No Contact page link found for {url}")
                    continue

                # Visit the Contact page and scrape emails
                emails = self.scrape_contact_page(contact_url)
                if emails:
                    self.results[contact_url] = emails
                    print(f"Emails found: {emails}")
                else:
                    print(f"No emails found on {contact_url}")

            except Exception as e:
                print(f"Error processing URL {url}: {e}")
                continue

        return self.results
