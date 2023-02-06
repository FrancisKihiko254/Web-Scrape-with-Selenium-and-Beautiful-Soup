# How to do Web Scraping using Selenium, Beautiful-Soup and Python
Web scraping is an automated technique of extracting data from websites.It can be in form of a text, image or other formats.Internet has enormous volume of data that if exracted, can be used for various purposes including Sentiment analysis, Market reasearch(Price comparison), Data Analysis, Lead generation, News monitoring and Social media analysis.We will be looking at how you can automate your data scraping task.
## Pre-requisite
1. **Selenium**   -is an open source framework for automating web browsers.It is often used for testing web application and scraping websites.  
3. **Beautiful Soup** - is a python library for extracting data from HTML and XML files. It is used to parse and extract data from unstructured or semi-structured sources.
4. Basic HTML knowledge

## Install selenium
``` 
pip install selenium 
```
## Install Beautiful Soup
``` 
pip install bs4 
```
We have installed the required packages and now we can dive into the coding part.
We will be scraping data from [olympedia](http://www.olympedia.org/) websites.
Suppose we want to analyze how men and wemen in athletics have performed in a given country, how many medals in each category(Gold, Bronze, Silver) they have won since the year 1900.In order to perform this task, we need data and the most reliable source we can get it is from [olympedia](http://www.olympedia.org/).Coping this data one by one manually will be a tedious work and may take many hours to complete,that is where web scraping come in handy.

![olympic](https://user-images.githubusercontent.com/107842949/216932859-d7f482f7-5b67-4d9d-8aef-4946a241f65c.JPG).

## STEP 1: Import the necessary packages
```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import csv
from bs4 import BeautifulSoup
```
## STEP 2:  Create chrome driver object and install chrome Driver manager
```
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```
 Assign the URL for the medals page:
 ```
 driver.get('http://www.olympedia.org/statistics/medal/country')
 ```
 ## STEP 3: Retrieving Form Elements
We must locate the elements and options necessary to update the table. The Selenium library has many tools for locating elements, circumstances may dictate a preferred path in some cases, but often there are several ways to achieve any objective. Here we’ve chosen to employ the .find_element('id','ID Name') method, which allows us to identify an element by its “id” string.

We can examine the source code of the page to identify an “id”, “class name” or any other feature by right-clicking the page in the browser window and selecting “inspect element”.

![inspect_element_view (1)](https://user-images.githubusercontent.com/107842949/216948254-a5f1cc60-8f17-4ec6-b392-a727a19ebd17.png)

In this view, we can navigate through all the elements and identify the “id”s we need. The dropdowns for the Olympic year and gender are labeled edition_select and athlete_gender respectively. We assign those elements to variables with the following lines:
```
year = driver.find_element('id','edition_select')

gender = driver.find_element('id','athlete_gender')
```
The next step, is to collect the options for those dropdowns, and we can do so with another locate method:
```
year_options = year.find_elements(By.TAG_NAME,'option')

gender_options = gender.find_elements(By.TAG_NAME,'option')
```
I the code below, we are going to use a nested loops, cycling through men and women first, and on the interior loop, clicking through the years for every summer games. We execute each selection by simply looping each of our option lists and calling the .click() method on the option object to submit that form selection.
```
for gender in gender_options[1:]:  # index 0 is omitted because it contains placeholder txt
   gender.click()

   for year in year_options[2:]: # skipping first two options to start with 1900 
       year.click()
```
Once we’ve made our selections we can pass the page source to Beautiful Soup by calling the .page_source attribute on our driver object to parse the content of this iteration of the page:
```
soup = BeautifulSoup(driver.page_source, 'html.parser')
```
## STEP 4: Parsing the Source 
With the page content in hand we must now locate the table elements of interest, so we can copy only those items to our output file. In order to isolate this content, we utilize two versions of Beautiful Soup’s search methods. First, we can grab the start of the row containing team USA results with the .find() method. In this instance, we use a regular expression as an argument to ensure we get the correct object. Next, we can use another variation of a search method, .find_all_next(<tag><limit>) to extract the medal counts. This method allows us to pull all of the objects that follow any other, and an optional <limit> argument gives us the flexibility to specify how many elements (beyond our reference) we’re interested in capturing.
 ```
head = the_soup.find(href=re.compile('USA'))
medal_values= head.find_all_next('td', limit=5)
 ```
 We have completed browser automation and with the head.find_all_next('td', limit=5) object we have access to the medal counts for each medal type as well as the overall total for that year. Now, all that remains is to bundle our data and set up our export pipeline. First, we process the data we’ve sourced by calling the .string attribute on the elements we’ve captured and assigning the result to a variable, medals_lst. Then we supplement the medal values with the year and gender values and append the entire thing to a list.
 
 ```
 try:
   year_val = year.get_attribute('text')
   head = the_soup.find(href=re.compile('USA'))

   medal_values = head.find_all_next('td', limit=5)
   val_lst = [x.string for x in medal_values[1:]] # the first index is the link with the country abbreviation and flag

except:
   val_lst = ['0' for x in range(4)] # we address years team USA did not compete with this option

val_lst.append(gender_val)
val_lst.append(year_val)

usa_lst.append(val_lst)
driver.quit()
 ```
 ## STEP 5: Finally we can save our data in csv format
 ```
 output_f = open('output.csv', 'w', newline='')
output_writer = csv.writer(output_f)

for row in usa_lst:
   output_writer.writerow(row)

output_f.close()
 ```
