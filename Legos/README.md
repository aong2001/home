### Legos

Libraries: `Pandas`, `bs4`, `requests`, and `selenium`

Project Legos collects information about Lego sets avaliable December 16, 2021. Originally, this was used to teach college freshman and sophomores about webscraping using Selenium to move around infinite scroll and other dynamic aspects of website design. 

Each Lego theme URL is collected then each URL is iterated using Selenium. From every Theme Page metadata about the theme is collected (e.g. total number of products). A pop-up appears for Cookie/Privacy Polciy acceptance; this is existed. Theme Pages utilize a "Show All" button and infinite scroll. First, the "Show All" button is clicked using `contains text`. Second, the infinite scroll is dealt with through a while look comparing beginning height to post-scroll height to find when the height stops changing (e.g. expected for the website to remain the same height after a scroll if the end of the page is reached). 

After all products on the Theme Page are visible individual product information is collected using `span` tags and `class` attributes. This information is entered into a dataframe. The dataframe is subsquently cleaned to create `float` columns were possible. Additionally, individual products that do not have information (e.g. stars and price) are dropped.
