### Company Clustering

Libraries: `Pandas`, `json`, `os`, 

Project Company Clustering uses the SEC's EDGAR REST API to pull filing company information. Company location information is then used in the Google API to find distances between companies within the United States. This project was originally created to teach juniors about accessing EDGAR data, data organization, and Google API access. 

EDGAR organizes filings according to Central Index Key (CIK) and offers a `txt` file of all used CIKs within the EDGAR database. General information is avaliable on EDGAR for every filing company using their CIK. First, this information is collected by reconstructing links to match EDGAR's format and `requests` is used to send a personal `header` to EDGAR and retrive a `json` of CIK specific information. This data is stored as `json` files. 

These "general" CIK files are iterated through to create a dataframe containing company specific data which does not vary across filings: headquarters address, SIC code, firm name, firm tickers, and fiscal year end. Additionally, whether the company has filed a 10-K, 10-Q, and/or 8-K is recorded as a `boolean`. This process creates an "address book" of companies (their address), a dataframe of their general information, and a dataframe containing every single filings for each CIK and the associated accession number (unique identifier of a EDGAR document). 

Files are then subset based on: (1) historically filing a 10-K and (2) being traded on either Nasdaq or NSYE. These firm's addresses are pulled from the address book. Google Map's API is then utilized to find the latitude and longitude of the address which is then recorded. This process creates a "coordinate databook". 

Next, the distances between each firm is calculating using Haversine's Distance Formula. Then are iterative clustering script is used to find groups of companies in the United States.

# FINISH 
