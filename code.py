import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re as re

options = Options()
options.add_argument("--headless")
driver = webdriver.Edge(options=options)
'''
try:
    driver.get("https://books.toscrape.com/")
    print(driver.title) 
    book_names = driver.find_elements(By.XPATH, "//h3/a")
    number_of_books = len(book_names)
    print(f"Number of books found: {number_of_books}")
    books_descriptions = []
    categories=[]
    books_info = []
    for i in range(number_of_books):
        urls = driver.find_elements(By.XPATH,'//h3/a')   
        current_book_page = urls[i]      
        current_book_page.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='product_description']/following-sibling::p")))
        description = driver.find_element(
            By.XPATH, "//div[@id='product_description']/following-sibling::p"
        ).text
        category = driver.find_element(By.XPATH, "//ul[@class='breadcrumb']/li[3]/a").text
        categories.append(category)
        product_info = {
            "UPC": driver.find_element(By.XPATH, "//table[@class='table table-striped']//tr[1]/td").text,
            "Product Type": driver.find_element(By.XPATH, "//table[@class='table table-striped']//tr[2]/td").text,
            "Price (excl. tax)": driver.find_element(By.XPATH, "//table[@class='table table-striped']//tr[3]/td").text,
            "Price (incl. tax)": driver.find_element(By.XPATH, "//table[@class='table table-striped']//tr[4]/td").text,
            "Tax": driver.find_element(By.XPATH, "//table[@class='table table-striped']//tr[5]/td").text,
            "Availability": driver.find_element(By.XPATH, "//table[@class='table table-striped']//tr[6]/td").text,
            "Number of reviews": driver.find_element(By.XPATH, "//table[@class='table table-striped']//tr[7]/td").text,
        }

        print(description)
        print(product_info)

        books_descriptions.append(description)
        books_info.append(product_info)
        driver.back()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3/a")))  
    book_names = driver.find_elements(By.XPATH, "//h3/a")
    book_prices = driver.find_elements(By.XPATH,"//div[@class='product_price']/p[@class='price_color']")
    books_status = driver.find_elements(By.XPATH,"//p[@class='instock availability']")
    books_star_ratings=  driver.find_elements(By.XPATH,"//p[contains(@class,'star-rating')]")
    
    for name, price, status, star_rating, description, product_info, category in zip(book_names,book_prices,books_status,books_star_ratings,books_descriptions,books_info,categories):
        rating = star_rating.get_attribute("class").replace("star-rating ", "").strip()
        print(f" Name: {name.get_attribute('title')}, Price: {price.text}, Status: {status.text}, Rating: {rating}, Description: {description}, Product Info: {product_info}, Category: {category}")

    with open("book_names.txt", "wb") as file:
        for name, price, status, star_rating, description, category, product_info in zip(book_names, book_prices, books_status, books_star_ratings, books_descriptions, categories, books_info):
            rating = star_rating.get_attribute("class").replace("star-rating ", "").strip()
            file.write(f"{name.get_attribute('title')}, {price.text}, {status.text}, {rating},{category},{description},{product_info}\n".encode())

finally:
    driver.quit()
'''
'''

try:
    driver.get("https://quotes.toscrape.com/")
    print("Successfully navigated to the quotes page.")
    print(driver.title)
    authord_infos = []
    authors_seen = set()
    target_count =21
    done = False
    x=0
    
    
    while len(authord_infos) < target_count:
        qoutes = driver.find_elements(By.CSS_SELECTOR,".quote")
        if len(authord_infos) >= target_count:
            break
        page_author_links = []
        for qoute in qoutes:
            name = qoute.find_element(By.CSS_SELECTOR,'.author').text.strip()
            if name not  in authors_seen:
                if not any(n ==name for n,u in page_author_links):
                    about_url = qoute.find_element(By.TAG_NAME, "a").get_attribute("href")
                    page_author_links.append((name, about_url)) 

        for name, url in page_author_links:
            if len(authord_infos)>= target_count:
                break  
            if name in authors_seen:
                continue
            authors_seen.add(name)
            driver.get(url)
            wait = WebDriverWait(driver,10)
            born_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.author-born-date'))).text
            born_location = driver.find_element(By.CSS_SELECTOR,'.author-born-location').text
            description = driver.find_element(By.CSS_SELECTOR,'.author-description').text.strip()

            authord_infos.append({ 
                'Name':name,
                 'Date of Birth':born_date,
                 'Nationality/Location':born_location,
                 'Description':description
            })
        if len(authord_infos) >= target_count:
            break
        driver.back()
        time.sleep(1)

        try:
            next_button = driver.find_element(By.XPATH,"//li[@class='next']/a")
            next_button.click()
            time.sleep(1)
        except Exception:
            print("No more page left to scape.")
        break

    print(f'{authors_seen}')
    print(f"{len(authors_seen)}")
    print(f" {len(page_author_links)}")   

finally:
    driver.quit()'''
try:
    url = "https://wikipedia.org/wiki/Special:Random"
    driver.get(url)

    wait = WebDriverWait(driver,10)

    title = wait.until(EC.presence_of_element_located((By.ID,"firstHeading"))) 
    page_title = title.text


    current_url  = driver.current_url
    paragraph = driver.find_elements(By.CSS_SELECTOR,'#mw-content-text  .mw-paser-output > p')
    article_intro = ''
    for p in paragraph:
        if p.text.strip():
            article_intro = p.text
            break
    print("=" *50)
    print(f'Random wiki page scrape')
    print("=" *50)
    print(f"Title: {page_title}")
    print(f"URL:  {current_url}")
    print(f"Introduction paragraph:\n{article_intro}")
    print("="*50)
    
finally:
    driver.quit()
