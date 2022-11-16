import pandas as pd
import json
import os
import ast

def address_book(cik_basic_file): 
    '''
    Creates structured format address information for EDGAR filing companies. 
    '''
    firm_name = cik_basic_file['name']
    all_address_info = cik_basic_file['addresses']
    mailing_address = all_address_info['mailing']  # simple dictionary creation
    business_address = all_address_info['business']

    address_book = {'mailing_street1': mailing_address['street1'],
                    'mailing_street2': mailing_address['street2'],
                    'mailing_city': mailing_address['city'],
                    'mailing_state': mailing_address['stateOrCountry'],
                    'mailing_zip': mailing_address['zipCode'],
                    'business_street1': business_address['street1'],
                    'business_street2': business_address['street2'],
                    'business_city': business_address['city'],
                    'business_state': business_address['stateOrCountry'],
                    'business_zip': business_address['zipCode']}

    return firm_name, address_book

def financial_metadata(cik_basic_file):
    '''
    Creates a structured format information about the filings for an EDGAR filing company. 
    '''
    form_types_filed = set(list(cik_basic_file['filings']['recent']['form']))

    try:
        has_10k = True if ('10-Q' in form_types_filed) else False
        has_10q = True if ('10-K' in form_types_filed) else False
        has_8k = True if ('8-K' in form_types_filed) else False
    except: 
        has_10k = False
        has_10q = False
        has_8k = False

    financial_data = {'sic_code': cik_basic_file['sic'],
                    'sic_description': cik_basic_file['sicDescription'],
                    'firm_name': cik_basic_file['name'],
                    'tickers': cik_basic_file['tickers'],
                    'exchanges': cik_basic_file['exchanges'],
                    'fiscal_end': cik_basic_file['fiscalYearEnd'],
                    '10K': has_10k, 
                    '10Q': has_10q, 
                    '8K': has_8k}
    return financial_data

def filings_book(cik_basic_file): 
    '''
    Creates a structured format of all the filings of an EDGAR filing company. 
    '''
    cik_num = cik_basic_file['cik']
    filings_info = cik_basic_file['filings']['recent']

    acc_numbers = filings_info['accessionNumber']
    dates = filings_info['filingDate']
    reporting_dates = filings_info['reportDate']
    forms = filings_info['form']
    filenums = filings_info['fileNumber']
    xlbrs = filings_info['isXBRL']
    inlinexlbrs =filings_info['isInlineXBRL']
    descriptions = filings_info['primaryDocDescription']

    filings_list = []
    for acc_index in range(len(acc_numbers)): 
        to_append = {'cik': cik_num,
                    'accession_number': acc_numbers[acc_index],
                    'filing_date': dates[acc_index],
                    'report_date': reporting_dates[acc_index],
                    'form_type': forms[acc_index],
                    'file_number': filenums[acc_index],
                    'xlbr_status': xlbrs[acc_index],
                    'inline_xlbr_status': inlinexlbrs[acc_index],
                    'document_desc': descriptions[acc_index]} 
        filings_list.append(to_append)
    return filings_list

curr_directory = os.getcwd()
import_path = curr_directory + '/Basic_CIK_Return'
os.chdir(import_path)

address_dataframe = pd.DataFrame()
financial_dataframe = pd.DataFrame()
filings_datalist = []
all_basic_files = os.listdir()  # get all of the files that contain basic information about companies

for i, filename in enumerate(all_basic_files):  # iterate through each of the files 
    cik = filename.split('.')[0]  # isolate the CIK from the filename
    try: 
        with open(filename) as json_file:
            cik_data = json.load(json_file)
    except: 
        print(filename)
        continue
    
    name, address_info = address_book(cik_data)  # return the bulk of the address information
    filer_info = financial_metadata(cik_data)
    filing_info = filings_book(cik_data)
    filings_datalist.extend(filing_info)

    address_info['cik'], filer_info['cik'] = cik, cik
    address_info['firm_name'] = name

    address_dataframe = address_dataframe.append(address_info, ignore_index = True)  # create a dataframe entry for each CIK 
    financial_dataframe = financial_dataframe.append(filer_info, ignore_index = True)
    
    if (i % 100) == 0: 
        print(i)

filings_dataframe = pd.DataFrame.from_dict(filings_datalist)
os.chdir(curr_directory)
address_dataframe.to_csv('address_book.csv')
financial_dataframe.to_csv('filer_information.csv')
filings_dataframe.to_csv('full_fillings_book.csv')
