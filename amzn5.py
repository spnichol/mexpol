# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 11:13:06 2017

@author: spnichol
"""

import pandas as pd
from numpy import nan
from re import findall,sub
import re 
from lxml import html
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random 


driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
#rev_df = pd.DataFrame(columns=['ProdID', 'Link', 'Rating', 'Text'])
#linkdf = pd.DataFrame(columns=['Link', 'Link_Status'])
def amzn_scrape(page):
    global rev_df, linkdf
    data = {'ProdID':[], 'Link':[], 'Rating': [], 'Text':[]}
    #page = "'"+page+"'"
    print page 
    driver.get(page)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    prod_id = re.search(r'\/[0-9A-Z]{10}', page).group(0)
    prod_id = prod_id.replace("/", "")
    for review in soup.find_all('div',attrs={"class" : "a-section celwidget"}):
        star = review.find('span',attrs={"class" : "a-icon-alt"})
    #    star = star.text
        rev_text = review.find('div',attrs={"class" : "a-section"})
        rev_text = rev_text.text
        data['ProdID'].append(prod_id)
        data['Link'].append(page)
        data['Rating'].append(star)
        data['Text'].append(rev_text)

    rev_df = rev_df.append(pd.DataFrame(data, columns=['ProdID', 'Link', 'Rating', 'Text']), ignore_index=True)
    links_temp = {'Link': [], 'Link_Status':[]}       

    for link in soup.find_all('a', href=True):
        link = link['href']
        if "amazon.com.mx" in link:
            print "link ok"
        else: 
            link = "https://www.amazon.com.mx"+link  

        r1 = re.compile(r"\/[0-9A-Z]{10}")
        if r1.search(link) and link not in linkdf['Link'] and r1.search(link) != prod_id:
            print "Yes, this is a valid link."
            links_temp['Link'].append(link)
            links_temp['Link_Status'].append("Added")
        else: 
            print link 
            print "No, this is some other type of link."
            links_temp['Link'].append(link)
            links_temp['Link_Status'].append("Trash")

    linkdf = linkdf.append(pd.DataFrame(links_temp, columns=['Link', 'Link_Status']), ignore_index=True)
    linkdf = linkdf.drop_duplicates()



for index, row in linkdf.iterrows():

    if row["Link_Status"] == "Added":
        print "scraping a new one" 
        wait_time = random.randint(1, 6)
        time.sleep(wait_time)
        row['Link_Status'] = "Newly_Scraped"#
        amzn_scrape(row["Link"])
    else:
        print "just trash or already scraped"

            
#for index, row in linkdf.iterrows():
#    r1 = re.compile(r"(?:RID=[0-9A-Z]*)")
#    link = row["Link"]
#    if r1.search(link):
#        row["Link_Status"] = "Added"
#    else:
#        pass 
#
