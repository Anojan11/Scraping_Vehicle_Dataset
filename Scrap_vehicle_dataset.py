#!/usr/bin/env python
# coding: utf-8

# In[5]:


#Reference
# https://www.analyticsvidhya.com/blog/2020/08/web-scraping-selenium-with-python/
# https://towardsdatascience.com/web-scraping-e-commerce-website-using-selenium-1088131c8541


#Importing libraries
import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import ElementClickInterceptedException
import numpy as np
import validators

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager #Firefox webdriver_manager


#Setting Folder to store downloaded images 
os.chdir('/Users/Anojan/Desktop/SenzMate/Webscrap/sc_img/')
baseDir=os.getcwd()


#Headless firefox browser
from selenium import webdriver 
opts = webdriver.FirefoxOptions()
opts.headless =True
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

count = 0
link_count = 2
while (link_count < 100):
    search_url="https://www.autotrader.co.uk/car-search?sort=relevance&postcode=so152gb&radius=1500&include-delivery-option=on&price-from=500&price-to=3000&year-to=2022&maximum-mileage=200000&page={}".format(link_count) 
    driver.get(search_url)

     #Scroll to the end of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)#sleep_between_interactions

    links=[]
    for dr in driver.find_elements_by_tag_name('div'):
        for a in dr.find_elements_by_tag_name('ul'):
            for q in a.find_elements_by_tag_name('li'):
                for j in q.find_elements_by_tag_name('article'):
                    for m in j.find_elements_by_tag_name('a'):
                        link = m.get_attribute('href')
                        links.append(link)
#     print(links)
    print(len(links))
    _links = np.unique(links).tolist()
    
    #Getting validaed URLs only, because some URLs are malformed URLs
    valid_links=[]
    for i in range (len(_links)):
        if validators.url(_links[i]):
            valid_links.append(_links[i])
            
     #Extracting corresponding link of img tag       
    for valid_link in valid_links:
        driver.get(valid_link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)#sleep_between_interactions
        img=[]
        for tag in driver.find_elements_by_tag_name('img'):
            img_link = tag.get_attribute('src')
            img.append(img_link)
        img = list(filter(None, img))
        _img = np.unique(img).tolist()
        _img = list(filter(lambda k: '.svg' not in k, _img))
        # print(len(_img),_img)
        
        #Downloading & save each image in the Destination directory
        for url in _img:
            if 'w100h75' in url:#Replacing size of the image
                url = url.replace("w100h75", "w800h600")
            file_name = "{}_{}.jpg".format(link_count,count)
            print(url)
            try:
                image_content = requests.get(url).content

            except Exception as e:
                print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")

            try:
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file).convert('RGB')

                file_path = os.path.join(baseDir, file_name)

                with open(file_path, 'wb') as f:
                    image.save(f, "JPEG", quality=100)
                print(f"SAVED - {url} - AT: {file_path}")
            except Exception as e:
                print(f"ERROR - COULD NOT SAVE {url} - {e}")
            count+=1   
    link_count+=1        


# In[ ]:




