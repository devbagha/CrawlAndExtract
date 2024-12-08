import time
import re
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor

# Start timer
start_time = time.time()

# Initialize the Chrome driver (we'll initialize it inside each thread later)
def initialize_driver():
    return webdriver.Chrome()


# Function to extract emails from text
def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

# Function to scrape contact page and extract emails
def scrape_contact_page(url):
    driver = initialize_driver()
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
            emails = extract_emails(page_source)
            result["emails"] = emails
        except NoSuchElementException:
            print(f"No Contact page link found for {url}")
    except Exception as e:
        pass
    finally:
        driver.quit()
    
    return result

# Initialize Selenium and search Google
driver = webdriver.Chrome()
driver.get("https://www.google.com")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

# Perform a search
search_box = driver.find_element(By.NAME, "q")
keyword = "Software companies usa"
search_box.send_keys(keyword)
search_box.send_keys(Keys.RETURN)

all_urls = []  # List to store URLs

# Extract URLs from the first page of search results
while True:
    time.sleep(5)
    results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
    print(f"Found {len(results)} results on this page.")
    
    for result in results:
        url = result.get_attribute("href")
        if url not in all_urls:  # Avoid duplicates
            all_urls.append(url)

    # Check if the "Next" button is available and click it
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "pnnext"))
        )
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
    except Exception:
        print("No more pages available.")
        break

driver.quit()

# Use ThreadPoolExecutor to scrape pages in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(scrape_contact_page, all_urls))

# Process the results into a Pandas DataFrame
data = []
for result in results:
    data.append([result["url"], "; ".join(result["emails"]) if result["emails"] else "No emails found"])

df = pd.DataFrame(data, columns=["Contact Page URL", "Emails"])

# Save the DataFrame to a CSV file
csv_file = "scraped_emails.csv"
df.to_csv(csv_file, index=False)

print(f"Data saved to {csv_file}")

# End timer
end_time = time.time()

# Calculate and print the total execution time
execution_time = end_time - start_time
print(f"Total execution time: {execution_time:.2f} seconds")
