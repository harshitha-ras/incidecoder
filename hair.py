from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd


def scrape_products(home_url, start_page, end_page, matches, wash_matches, cat):
    '''
    Steps:

    1. Iterate through the pages
    2. For every page, Find the attribute for the products
    3. find all the class of all products on the page
    4. Store the link and name of the product
    5. if the name of the product has the word hair in it, and wash words are in it, append.
    6. else if the name of the product has no stop words, go into the link of the product:
    7. if the desc has the word hair in it, and it doesn't have wash words in it, append.
    8. else if the desc doesn't any stop words, append.
    Not included anymore--9. else if it says hair anywhere on the page, append.
    10. Products loop when the find all function ends
    11. Pages loop will end if there are no more products on the page

    Include in next iteration: check if the product was already checked by adding to a unique set?

    Arguments used:
        home_url (str): The base URL of the site to scrape.
        start_page (int): The starting page number for scraping.
        end_page (int): The ending page number for scraping.
        matches (list): List of words to reject.
        wash_matches (list): List of words to exclude.
        cat (str): Category word to filter products.

    Returns:
        tuple: A tuple containing a list of accepted products and rejected products.

    '''

    # Initialize the WebDriver instance
    driver = webdriver.Chrome()

    matches = ["skin", "eye", "face","lip", "body", "age", "wrinkle", "facial", "spf", "firming", "breakout", "shave", "primer", "acne", "powder"]
    wash_matches = ["shampoo", "conditioner"]
    cat = "hair"
    products = []  # List to store names of the accepted products
    reject = [] # List to store names of the rejected products
    home_url = "https://incidecoder.com/ingredients/niacinamide?uoffset="
    p_count = 0  # counter to iterate through the accepted products list
    r_count = 0 # counter to iterate through the accepted products list
    product_no = 0 # counting number of products that were checked

    #MAIN-------------------------------------------------------------------------------------------------------------------------
    # Iterating pages and products to find target_word
    for page in range(258, 259, 1):
        #Get page link
        print("page=", page)
        url = home_url + str(page)
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")

        # extracting product using attributes
        product_links = soup.find_all("a", href=True, attrs={'class': "klavika simpletextlistitem"})

        #store the product name and link
        for a in product_links:
            product_no = product_no+1

            name = a.text.lower()
            link = a.get('href')
            
            # check product name if it matches the condition
            if cat in name and not any(word.lower() in name for word in wash_matches):
                print("accept code 1")
                products.append(name)
                p_count = p_count+1
            elif not any(word.lower() in name for word in matches):

            # Navigate to the product link and check if it contains the target_word
                driver.get("https://incidecoder.com" + link)
                product_url = driver.page_source
                sub_soup = BeautifulSoup(product_url, features='html.parser')
                desc = sub_soup.find('span', class_='showmore-section', id='showmore-section-ingredlist-details')
                if desc is not None:
                    if cat in desc.text.lower() and not any(word.lower() in name for word in wash_matches):
                        products.append(name)
                        print("accept code 2")
                        p_count = p_count+1
                    elif not any(word.lower() in desc.text.lower() for word in matches):
                        print("accept code 3")
                        products.append(name)
                        p_count = p_count+1
            else:
                reject.append(name)
                r_count = r_count+1
                print("reject code")
                        

    # Close the WebDriver instance after the script finishes
    driver.quit()
    return products, reject


def save_to_csv(products, reject):
    """
    Saves the accepted and rejected products to CSV files.

    Arguments used:
        products (list): List of accepted product names.
        reject (list): List of rejected product names.
    """
    # Creating a DataFrame and saving to CSV
    df = pd.DataFrame({'Product Name': products})
    df.to_csv('products.csv', index=False, encoding='utf-8')

    rdf = pd.DataFrame({'Reject Name': reject})
    rdf.to_csv('reject.csv', index=False, encoding='utf-8')


def main():
    # Set default values
    home_url = "https://incidecoder.com/ingredients/niacinamide?uoffset="
    start_page = 1
    end_page = 1
    matches = ["skin", "eye", "face", "lip", "body", "age", "wrinkle", "facial", "spf", "firming", "breakout", "shave", "primer", "acne", "powder"]
    wash_matches = ["shampoo", "conditioner"]
    cat = "hair"

    products, reject = scrape_products(home_url, start_page, end_page, matches, wash_matches, cat)
    save_to_csv(products, reject)


if __name__ == "__main__":
    main()