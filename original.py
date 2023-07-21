from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By

'''
Steps:

1. Iterate through the pages
2. For every page, Find the attribute for the products
3. find all the class of all products on the page
4. Store the link and name of the product
5. if the name of the product has the word hair in it, append.
6. else if the name of the product has any stop words, break.
7. else if, go into the link of the product.
8. if the desc of the product has any stop words, break.
9. else if it says hair anywhere on the page, append.
10. Products loop when the find all function ends
11. Pages loop will end if there are no more products on the page

check if the product was already checked by adding to a unique set?
'''

driver = webdriver.Chrome()

matches = ["skin", "eye", "lip", "age", "wrinkle", "facial", "face", "spf", "firming", "breakout", "shave", "primer"]
word_to_find = "hair"
products=[] #List to store name of the product
home_url = "https://incidecoder.com/ingredients/niacinamide?uoffset="

#iterating products to find target_word
def has_word(link, target_word):
    driver.get("https://incidecoder.com"+link)
    product_url = driver.page_source
    sub_soup = BeautifulSoup(product_url, features='html.parser')
    result = target_word in sub_soup.get_text()
    desc = sub_soup.find('span', class_='showmore-section', id='showmore-section-ingredlist-details')
    if result and desc and not any([word.lower() in desc.text.lower() for word in matches]):
        return result

#iterating pages
for page in range(1, 342, 1):
    print("page=", page)
    url = home_url + str(page)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    

    #<a href="/products/clio-kill-cover-founwear-foundation" class="klavika simpletextlistitem" data-ga-eventcategory="ingredient-product" data-ga-eventlabel="product:clio-kill-cover-founwear-foundation">Clio Kill Cover Founwear Foundation</a>

    for a in soup.find_all("a",href=True, attrs={'class':"klavika simpletextlistitem"}):
        name = a.text.lower()
        link = a.get('href')
        
        if has_word(link, word_to_find):
            print(name)
            products.append(name)

        
    


    
#<a href="/ingredients/cyclohexasiloxane?uoffset=1" data-ga-eventcategory="ingreient-product-next">Next page &gt;&gt;</a>
#<a href="/ingredients/cyclohexasiloxane?uoffset=2">Next page &gt;&gt;</a>


	
df = pd.DataFrame({'Product Name':products}) 
#print(df)
df.to_csv('products.csv', index=False, encoding='utf-8')