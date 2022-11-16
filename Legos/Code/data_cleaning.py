import pandas as pd
import math
import numpy as np

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
