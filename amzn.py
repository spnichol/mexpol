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
rev_df = pd.DataFrame(columns=['ProdID', 'Link', 'Rating', 'Text'])
prod_df = pd.DataFrame(columns=['ProdID', 'Status'])
#linkdf = pd.DataFrame(columns=['Link', 'Link_Status', 'ProdID'])
def amzn_scrape(prodid):
    global rev_df, linkdf, prod_df
    prod_temp = {'ProdID':[], 'Status':[]}

    page = "https://www.amazon.com.mx/dp/" + prodid +"/"
    print page 
    driver.get(page)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    prod_id = re.search(r'\/[0-9A-Z]{10}', page).group(0)
    prod_id = prod_id.replace("/", "")
    for link in soup.find_all('a', href=True):
            link = link['href']         
            if "amazon.com.mx" in link and r1.search(link):
                prod_link_id = re.search(r'\/[0-9A-Z]{10}', link).group(0)
                prod_link_id = prod_link_id.replace("/", "")
                if prod_link_id not in prod_df['ProdID']:
                    prod_temp['ProdID'] = prod_link_id
                else:
                    print "already in db"
                
            else: 
                print "not a product"

    prod_df = prod_df.append(pd.DataFrame(prod_temp, columns=['ProdID', 'Status']), ignore_index=True)


    
def get_reviews(prod_id):
    global rev_df, linkdf
    data = {'ProdID':[], 'Link':[], 'Rating': [], 'Text':[]}
    prod_link = "https://www.amazon.com.mx/product-reviews/" + prod_id + "/ref=cm_cr_getr_d_paging_btm_2?ie=UTF8&pageNumber=1&pageSize=100"
    driver.get(prod_link)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    num_revs = soup.find('span',attrs={"class" : "a-size-medium totalReviewCount"})
    num_revs = int(num_revs.text)
    print num_revs   
    for review in soup.find_all('div',attrs={"class" : "a-section celwidget"}):
        star = review.find('span',attrs={"class" : "a-icon-alt"})
        rev_text = review.find('div',attrs={"class" : "a-section"})
        rev_text = rev_text.text
        data['ProdID'].append(prod_id)
        data['Link'].append(page)
        data['Rating'].append(star)
        data['Text'].append(rev_text)
        
    rev_df = rev_df.append(pd.DataFrame(data, columns=['ProdID', 'Link', 'Rating', 'Text']), ignore_index=True)
        
#
#for index, row in linkdf.iterrows():
#
#    if row["Link_Status"] == "Added":
#        print "scraping a new one" 
#        wait_time = random.randint(1, 6)
#        time.sleep(wait_time)
#        row['Link_Status'] = "Newly_Scraped"#
#        amzn_scrape(row["Link"])
#    else:
#        print "just trash or already scraped"
#
#
