import requests
import os
import json
import time

def collect_basic_info(cik): 
    '''
    Collects a range of company information from the EDGAR site about each organization and returns the dictionaryy. 
    '''

    begin_base_url = 'https://data.sec.gov/submissions/CIK'
    end_base_url = '.json'

    request_url = begin_base_url + cik + end_base_url  # builds the URL which will be sent to EDGAR

    session = requests.Session()
    session.headers.update({'User-Agent': 'University of Texas at Austin alexnelson@utexas.edu'})

    return_data = session.get(request_url)  # requests the CIK using the reconstructed URL and user-agency

    return return_data.text

with open('cik_tickers.json', 'r') as file:  # SEC produced file of all SEC CIKs
    cik_relations = json.load(file)

curr_directory = os.getcwd()
export_path = curr_directory + '/Basic_CIK_Return'
os.chdir(export_path)

for i, index in enumerate(cik_relations.keys()):  # iterates through every CIK 
    start_time = time.time()
    cik = str(cik_relations[index]['cik_str'])
    neccesary_length = 10
    while len(cik) != neccesary_length:  # CIK input must be a length of 10 with 0s in front to create the length if neccesary
        cik = '0' + cik
    entered_cik = cik

    file = collect_basic_info(entered_cik)

    file_path = entered_cik + '.json'

    with open(file_path, 'w') as outfile:
        outfile.write(file)
    end_time = time.time()

    if ((end_time - start_time) < 0.15):  # prevents sending more than 10 requests per second (with a cushion)
        time.sleep(0.1)

os.chdir(curr_directory)
