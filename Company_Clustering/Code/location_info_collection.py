import pandas as pd
import numpy as np
import requests
import time

def filter_by_exchange(filer_df, location_df):
    '''
    Filter all EDGAR filers by those that file 10Ks and trades on Nasdaq or NSYE and is headerquartered in the US. 
    ''' 
    
    acceptable_ciks = []
    for i, filer in filer_df.iterrows():
        status_10k = int(filer['10K'])
        exchanges_traded = filer['exchanges']

        if (status_10k == 1) and (('Nasdaq' in exchanges_traded) or ('NYSE' in exchanges_traded)): 
            acceptable_ciks.append(filer['cik'])
    
    traded_locations = location_df[location_df['cik'].isin(acceptable_ciks)].reset_index()
    traded_locations = traded_locations.dropna().reset_index(drop = True)
    traded_locations = traded_locations[traded_locations['business_state'].str.isalpha()]
    
    return traded_locations
    
def get_location(address): 
    '''
    Returns the latitude and longitude of an input address. 
    '''
    google_api_key = 'AIzaSyDe6JprZ9x3zFxGDoY0Q6g6T9xHiTc9Z2Y'
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={google_api_key}"

    r = requests.get(endpoint)
    status = r.json()['status']
    if status != 'OK': 
        return None, None, None

    results = r.json()['results'][0]

    lat = results['geometry']['location']['lat']
    lng = results['geometry']['location']['lng']
    official_address = results['formatted_address']

    return lat, lng, official_address

locations_df = pd.read_csv('address_book.csv')
filer_df = pd.read_csv('filer_information.csv')
filtered_locations = filter_by_exchange(filer_df, locations_df)

location_dicts = []
for i, firm in filtered_locations.iterrows(): 
    begin_time = time.time()
    address1 = firm['business_street1']
    city = firm['business_city']
    state = firm['business_state']
    zipcode = firm['business_zip']

    entered_address = f"{address1}, {city}, {state}, {zipcode}"
    latitude, longitude, address = get_location(entered_address)

    to_append = {'cik': firm['cik'], 
                'latitude': latitude, 
                'longitude': longitude, 
                'official_address': address}
    print(to_append)
    location_dicts.append(to_append)
    end_time = time.time()

    if (end_time - begin_time) < 0.15: 
        time.sleep(0.1)

    if (i % 100) == 0: 
        print(i)

coordinate_dataframe = pd.DataFrame.from_dict(location_dicts)
coordinate_dataframe.to_csv('cordinates_databook.csv')
