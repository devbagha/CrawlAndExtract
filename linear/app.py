from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException  # Import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

start_time = time.time()
# Initialize the Chrome driver
driver = webdriver.Chrome()

try:
    # Open Google
    driver.get("https://www.google.com")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

    # Search for the query
    search_box = driver.find_element(By.NAME, "q")
    keyword = "Software companies usa"
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    all_urls = []  # To store all extracted URLs

    while True:
        time.sleep(5)
        # Extract all search result URLs on the current page
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

    # Print all collected URLs
    print("Collected URLs:")
    for url in all_urls:
        print(url)

finally:
    # Close the browser
    driver.quit()



def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)


import re
driver = webdriver.Chrome()

results = {}

try:
    for url in all_urls:
        
        try:
            print(f"Visiting: {url}")
            driver.get(url)
            time.sleep(2)  # Let the page load
        except:
            continue
        # Try to find a "Contact" page link
        try:
            contact_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Contact")
            contact_url = contact_link.get_attribute("href")
            print(f"Contact page found: {contact_url}")
        except:
            print(f"No Contact page link found for {url}")
            continue

        # Visit the Contact page
        try:
            driver.get(contact_url)
            time.sleep(2)  # Let the page load

            # Scrape emails from the page source
            page_source = driver.page_source
            emails = extract_emails(page_source)
            if emails:
                results[contact_url] = emails
                print(f"Emails found: {emails}")
            else:
                print(f"No emails found on {contact_url}")
        except:
            continue

finally:
    driver.quit()

# Print the results
print("Scraped Contact Page Emails:")
for contact_url, emails in results.items():
    print(f"{contact_url}: {emails}")

    # File name for the CSV
csv_file = "scraped_emails.csv"

# Write data to CSV
import csv

# with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     # Write the header row
#     writer.writerow(["Contact Page URL", "Emails"])

#     # Write each contact URL and its associated emails
#     for contact_url, emails in results:
#         # Join multiple emails with a semicolon for easy reading
#         writer.writerow([contact_url, "; ".join(emails)])

print(f"Data saved to {csv_file}")

end_time = time.time()

# Calculate and print the total execution time
execution_time = end_time - start_time
print(f"Total execution time: {execution_time:.2f} seconds")