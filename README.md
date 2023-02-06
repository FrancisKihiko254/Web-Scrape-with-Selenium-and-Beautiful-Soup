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

##STEP 1: Import the necessary packages
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
## STEP 2:  Create chrome driver object and install the compatible chrome Driver manager
```
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```
