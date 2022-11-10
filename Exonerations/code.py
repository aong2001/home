### IMPORT STATEMENTS ###
import pandas as pd
import numpy as np 
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

### DATA COLLECTION ###
url = 'https://www.law.umich.edu/special/exoneration/Pages/detaillist.aspx'
website = requests.get(url)
exoneration_soup = BeautifulSoup(website.text, 'html.parser')

cell_tags = exoneration_soup.find_all('td', class_ = 'ms-vb2')

nondata_index = []
unique_cases = []
for tag_index, cell_tag in enumerate(cell_tags):
    try:
        case_id_dirty = cell_tag.parent()[0].find('a').get('href')
        case_id = case_id_dirty.split('=')[1]
        unique_cases.append(case_id)
    except: 
        nondata_index.append(tag_index)
del cell_tags[min(nondata_index):max(nondata_index) + 1]

exonerations_data = pd.DataFrame(columns = ['case_id', 'last_name', 'first_name', 'age', 'race', 'state', 
                                            'county', 'tags', 'om_tags', 'crime', 'sentence', 'convicted', 
                                            'exonerated', 'DNA', 'centrality', 'MWID', 'FC', 'P/FA', 'F/MFE', 
                                            'OM', 'ILD'])

exoner_tracking = defaultdict(list)
for cell_tag in cell_tags: 
    case_id_dirty = cell_tag.parent()[0].find('a').get('href')
    case_id = case_id_dirty.split('=')[1]
    data = cell_tag.text
    if len(data) == 0: 
        data = ''
    
    exoner_tracking[case_id].append(data)   
    
for unique_key in list(exoner_tracking.keys()): 
    key_data = exoner_tracking[unique_key]
    if len(key_data) != 20: 
        print('------ THERE IS AN ERROR IN THE DATA ------')
    first_term = exoner_tracking[unique_key][0]
    letter_check = [True for letter in first_term if letter.isalpha()]
    if all(letter_check) == False:
        print('------ THERE IS AN ERROR IN THE DATA ------')
    key_data.insert(0, unique_key)
    exonerations_data.loc[len(exonerations_data)] = key_data
    
exonerations_data.to_csv('exonerations_data.csv')
