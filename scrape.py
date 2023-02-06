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

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('http://www.olympedia.org/statistics/medal/country')
year_dd = driver.find_element('id','edition_select')

gender_dd = driver.find_element('id','athlete_gender')
year_options = year_dd.find_elements(By.TAG_NAME,'option')

gender_options = gender_dd.find_elements(By.TAG_NAME,'option')
usa_lst=[]
for gender in gender_options[1:]:  # index 0 is omitted because it contains placeholder txt
   gender.click()
   time.sleep(2)
   for year in year_options[2:]: # skipping first two options to start with 1900 
       year.click()
       time.sleep(2)
       try:
          year = year.get_attribute('text')
          gender = gender.get_attribute('text')
          the_soup = BeautifulSoup(driver.page_source, 'html.parser')
          head = the_soup.find(href=re.compile('USA'))
          medal_values= head.find_all_next('td', limit=5)
          val_lst = [x.string for x in medal_values[1:]] # the first index is the link with the country abbreviation and flag
          #val_lst = ['0' for x in range(4)] # we address years team USA did not compete with this option
       except:
          val_lst = ['0' for x in range(4)] # we address years team USA did not compete with this option

       val_lst.append(gender)
       val_lst.append(year)

       usa_lst.append(val_lst)
       output_f = open('output.csv', 'w', newline='')
       output_writer = csv.writer(output_f)
       output_writer.writerow(['Gold', 'Silver', 'Bronze', 'Total','Gender','Year'])
for row in usa_lst:
   output_writer.writerow(row)
output_f.close()