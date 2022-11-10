
import pandas as pd 
import numpy as np
import requests
from bs4 import BeautifulSoup
import shortuuid
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import math

def selenium_extraction(reconstructed_url):
    '''
    Opens a Selenium Google Chrome page to utilize the infinite scroll down the page. 
    Return: The full HTML for the fully scrolled webpage. 
    '''
    driver_path = './chromedriver 6'                                                        # driver path; assuming the driver is in the same folder as this code
                                                                                            # if you are running on a windows us the .exe filename instead

    options = webdriver.ChromeOptions()                                                     # creating the webdriver that will automate the Chrome page
    driver = webdriver.Chrome(executable_path = driver_path, options = options)
    driver.get(reconstructed_url)  

                                                                                            # gets the xpaths for the cookie and privacy acceptance shadow screens 
    continue_button_path = '//*[@id="root"]/div[5]/div/div/div[1]/div[1]/div/button'
    privacy_button_path = '/html/body/div[4]/div/aside/div/div/div[3]/div[1]/button[1]'

    driver.find_element_by_xpath(continue_button_path).click()                              # uses ".click()" to select the button 
    time.sleep(5)
    driver.find_element_by_xpath(privacy_button_path).click()                               # same here

    time.sleep(5)
    
                                                                                            # the footer on the Lego website is pretty large so 
    footer_path = '//*[@id="root"]/footer/div[1]/div/div/div[1]'                            # xpath of the entire footnote area
    footer_dimensions = driver.find_element_by_xpath(footer_path).size                      # returns a dictionary of the dimensions
    footer_length = footer_dimensions['height']                                             # access the height key
    full_page_length = driver.execute_script("return document.body.scrollHeight")           # get the full height of the page including the footnote
    bottom_page = full_page_length - (1.85 * footer_length)                                 # footer takes up the entire page 
    driver.execute_script('window.scrollTo(0, ' + str(bottom_page) + ')')

    time.sleep(5)
    driver.find_element_by_xpath("//a[contains(text(), 'Show All')]").click()               # find an xpath by its text

    old_prefooter_height = bottom_page                                                      # this scrolls to the bottom of the page and waits for loading
    still_scrollable = True
    while still_scrollable == True: 
        time.sleep(5)
        full_page_length = driver.execute_script("return document.body.scrollHeight")
        bottom_page = full_page_length - (1.85 * footer_length)
        driver.execute_script('window.scrollTo(0, ' + str(bottom_page) + ')')
        time.sleep(5)

        new_prefooter_height = (driver.execute_script("return document.body.scrollHeight") - footer_length)
        if new_prefooter_height == old_prefooter_height: 
            still_scrollable = False
        else: 
            old_prefooter_height = new_prefooter_height
            still_scrollable = True

    html = driver.execute_script("return document.body.innerHTML;")                         # collect all of the HTML
    theme_soup = BeautifulSoup(html, 'html.parser')                                         # create a BSoup
    driver.quit()                                                                           # close the Selenium page
    
    return theme_soup
  
 themes_link = 'https://www.lego.com/en-us/themes'                                           # collects the general theme page 
html_doc = requests.get(themes_link)
soup = BeautifulSoup(html_doc.text, 'html.parser')

themes = soup.find_all('article')
theme_extensions = []
for theme_block in themes: 
    link_sublocation = theme_block.find('a')
    theme_extension = link_sublocation.get('href')                                          # gets the hyperlink extensions 
    theme_extensions.append(theme_extension)
    
product_data = pd.DataFrame(columns = ['timestamp', 
                                       'collection_id', 
                                       'name', 
                                       'stars', 
                                       'price', 
                                       'section_name'])
completed_urls = []

for ext in theme_extensions:                                                                # iterate through the URL extensions
    reconstructed_url = 'https://www.lego.com' + ext
    if reconstructed_url in completed_urls: 
        continue                                                                            # if the link has already been collected skip
        
    html = requests.get(reconstructed_url)
    theme_soup = BeautifulSoup(html.text, 'html.parser')
                                                                                            # get the "stats" summary from the top of the page "Showing 1 - 12 of 24"
    section_summary = theme_soup.find('div', class_ = 'Summary__Wrapper-sc-1ki9luf-0 hhbKIP')
    product_stats = section_summary.find('span', class_ = 'Text__BaseText-sc-178efqu-0 gFrusw').text
    segmented_stats = product_stats.split(' ')
    
    possible_max = [partial for partial in segmented_stats if partial.isnumeric() == True]  # list comprehension extracting only numbers from the split string 
    total_products = int(possible_max[-1])                                                  # find the number of products total within a section
    showed_products = int(possible_max[-2])                                                 # find the number of products showed on the page
    if total_products != showed_products: 
        try:
            theme_soup = selenium_extraction(reconstructed_url)                             # feeds selenium function defined above
        except: 
            theme_soup = selenium_extraction(reconstructed_url)
                                                                                            # find the entire grid of products on the screen
    product_grid = theme_soup.find('ul', class_ = 'ProductGridstyles__Grid-lc2zkx-0 gxucff')  
    product_sections = product_grid.find_all('li')               
    section_name = reconstructed_url.split('/')[-1]                                         # deconstruct the URL to get the name of Lego section
    
    for product in product_sections:                                                        # some cells are ads so we need to embed all actions in try-except statements
        product_info = {}
        try: 
            product_name = product.find('span', class_ = 'Markup__StyledMarkup-ar1l9g-0 hlipzx')
            product_name = product_name.text
            product_info['name'] = product_name
        except: 
            product_info['name'] = None

        try:
            star_count = product.find('div', class_ = 'RatingBarstyles__RatingContainer-sc-11ujyfe-2 fgbdIf')
            star_count = star_count.get('title')
            product_info['stars'] = star_count
        except:
            product_info['stars'] = None

        try:
            product_price = product.find('div', class_ = 'ProductPricestyles__Wrapper-vmt0i4-1 dEqmbq')
            product_price = product_price.text
            product_info['price'] = product_price
        except: 
            product_info['price'] = None

        product_info['collection_id'] = shortuuid.uuid()                                  # random ID incase we want to do more with the data later
        product_info['timestamp'] = time.time()                                           # timestamp just in case
        product_info['section_name'] = section_name
        product_data = product_data.append(product_info, ignore_index = True)             # append all of the data 
    completed_urls.append(reconstructed_url)
    
if len(completed_urls) == len(theme_extensions):
    print('---------------- ALL URLS HAVE BEEN SEARCHED FOR PRODUCT DATA ----------------')
    product_data.to_csv('lego_product_data.csv')                                          # produce the dataframe of raw uncleaned data
else: 
    print('----------------------- DATA COLLECTION IS NOT COMPLETE -----------------------')
    
    
product_data = pd.read_csv('lego_product_data.csv')                              # read in the raw data CSV file
if 'Unnamed: 0' in product_data.columns: 
    product_data = product_data.drop(columns = ['Unnamed: 0'])                   # drop the added unnamed column

price_adj = product_data['price']                                                # take an array of the price data current format is, "Price$##.###"
new_prices = []
for price in price_adj                                                           # iterate thru each price
    new_word = ''                                                                # empty string
    price = str(price)
    for letter in price:                                                         # go thru each letter in the old string
        if letter.isdigit() or letter == '.':                                    # only append to the new string if the substring (one char) is a decimal or number
            new_word += letter
    if len(new_word) == 0:                                                       # append nothing if the word is empty (so the data does not get mixed)
        new_prices.append(None)  
    else: 
        new_prices.append(float(new_word))                                       # turn into a float
product_data['price'] = new_prices

indices_remove = []

for row_index in range(len(product_data)):                                       # iterate thru each row
    datarow = product_data.iloc[row_index]                                       # collect row data
    star_count = float(datarow['stars'])
    product_price = float(datarow['price'])
    if math.isnan(star_count) and math.isnan(product_price):                     # if both price and star count is NaN drop the row -- it gives us no information
        indices_remove.append(row_index)
product_data = product_data.drop(indices_remove, axis = 0)                       # remove all of the columns at once
product_data = product_data.reset_index()
product_data.to_csv('cleaned_lego_product_data.csv')                             # export the cleaned CSV
        
