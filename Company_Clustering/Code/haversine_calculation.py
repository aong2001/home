import numpy as np
import pandas as pd
import time
import json

def calculate_haversine(lat1, lon1, lat2, lon2):
    '''
    Calculates the distance between two points. 
    '''
    radius_miles = 3963  # radius, in miles, of the earth

    rlat1, rlat2 = lat1 * (np.pi/180), lat2 * (np.pi/180)  # convert to radians
    rlon1, rlon2 = lon1 * (np.pi/180), lon2 * (np.pi/180)

    delta_lat = rlat1 - rlat2
    delta_lon = rlon1 - rlon2 

    # calculation of haversine distance
    a = (np.sin(delta_lat/2) ** 2) + np.cos(rlat1) * np.cos(rlat2) * (np.sin(delta_lon/2) ** 2)
    c = 2 * np.arctan2((a**0.5), ((1 - a)**0.5))
    d = radius_miles * c

    return d 

company_locations = pd.read_csv('coordinates_databook.csv')
ciks, latitudes, longitudes = company_locations['cik'], company_locations['latitude'], company_locations['longitude']

cik_distances = {}
for i, firm_cik in company_locations.iterrows():  # iterate through each company coordinates
    distances = []
    cik1 = firm_cik['cik']
    latitude1 = firm_cik['latitude']
    longitude1 = firm_cik['longitude']
    
    for cik2, latitude2, longitude2 in zip(ciks, latitudes, longitudes):  # iterate through all of the CIKs
        miles_distance = calculate_haversine(latitude1, longitude1, latitude2, longitude2)   # calculate the haversine distance between the first CIK and second
        distances.append((cik2, miles_distance))  # append the distance with the CIK
    cik_distances[cik1] = distances

    if (i % 100) == 0: 
        print(i)

file_path = 'usa_cik_distances.json'
with open(file_path, "w") as outfile:
    json.dump(cik_distances, outfile)
