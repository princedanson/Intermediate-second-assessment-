from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver (Make sure you have Chrome/Chromium installed)
driver = webdriver.Chrome()

base_url = "https://quotes.toscrape.com"
driver.get(base_url)

authors_data = []
seen_authors = set()
target_count = 15  # Adjust between 10 and 20 as needed

try:
    while len(authors_data) < target_count:
        # Find all quote elements on the current page
        quotes = driver.find_elements(By.CLASS_BAR, "quote") or driver.find_elements(By.CSS_SELECTOR, ".quote")
        
        # We need to extract the 'about' URLs first because navigating away 
        # breaks the element references on the main page (StaleElementReferenceException)
        page_author_links = []
        for quote in quotes:
            name = quote.find_element(By.CSS_SELECTOR, ".author").text
            if name not in seen_authors:
                # Get the link to the (about) page
                about_url = quote.find_element(By.TAG_NAME, "a").get_attribute("href")
                page_author_links.append((name, about_url))
        
        # Visit each new author's page to gather details
        for name, url in page_author_links:
            if len(authors_data) >= target_count:
                break
                
            seen_authors.add(name)
            driver.get(url)
            
            # Wait for elements on the bio page to load
            wait = WebDriverWait(driver, 10)
            born_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".author-born-date"))).text
            born_location = driver.find_element(By.CSS_SELECTOR, ".author-born-location").text
            description = driver.find_element(By.CSS_SELECTOR, ".author-description").text.strip()
            
            # Save the gathered profile fields
            authors_data.append({
                "Name": name,
                "Date of Birth": born_date,
                "Nationality/Location": born_location.replace("in ", ""), # Clean up 'in' prefix
                "Description": description[:150] + "..." # Truncated for display
            })
            
            # Go back to the main quotes listing page
            driver.back()
            time.sleep(1) # Polite scraping pause
            
        # Check if we hit the target; if not, go to the next page
        if len(authors_data) < target_count:
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, ".pager .next a")
                next_button.click()
                time.sleep(1)
            except Exception:
                print("No more pages left to scrape.")
                break

finally:
    # Always shut down the browser window when finished
    driver.quit()

# Print the final list of distinct authors
print(f"\nSuccessfully collected {len(authors_data)} distinct authors:\n")
for index, author in enumerate(authors_data, start=1):
    print(f"{index}. {author['Name']}")
    print(f"   DOB: {author['Date of Birth']}")
    print(f"   Nationality/Location: {author['Nationality/Location']}")
    print(f"   Bio Preview: {author['Description']}\n")
