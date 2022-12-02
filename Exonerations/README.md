### Exonerations

Libraries: `Pandas`, `requests`, and `bs4`

This project utilized [this](https://www.law.umich.edu/special/exoneration/Pages/detaillist.aspx) University of Michigan database of exonerations in the United States. The page is already structured like a data table so this process was quite simple. Each row is parsed through to see if it matches the static size requirements to be considered "data". If these requirements are met than the data is appended into the final CSV.

The program parses through the webpage and uses `td` tags and a `class` attribute to identify cells within the webpage structure. Then utilizing the structure of the webpage table iterates through the collected elements transferring them into a dataframe. Data is verified to be complete before entered into the dataframe. 
