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
import psycopg2
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
#rev_df = pd.DataFrame(columns=['ProdID', 'Link', 'Rating', 'Text'])
prod_df = pd.DataFrame(columns=['ProdID', 'Status', 'Title', 'Duplicate', 'Category', 'Sub'])

def amzn_scrape(prodid):
    global rev_df, linkdf, prod_df
    import re 
    prod_temp = {'ProdID':[], 'Status':[]}

    page = "https://www.amazon.com.mx/dp/" + prodid +"/"
    page = str(page)
    print page 
    driver.get(page)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    for link in soup.find_all('a', href=True):
        link = link['href']
        new = "'"+link+"'"
        if bool(re.search('=B[0-9A-Z]{9}', new)) == True:
            prod_link_id = re.search('=B[0-9A-Z]{9}', new).group(0)
            prod_link_id =prod_link_id.replace("=", "")

            if prod_link_id not in prod_df['ProdID'] and bool(re.search('[A-Z]', prod_link_id)) == True:
                prod_temp['ProdID'].append(prod_link_id)
                prod_temp['Status'].append("Added")
            else: 
                print "invalid page" 
        elif bool(re.search("\/B[A-Z0-9]{9}", new)) == True:
            prod_link_id = re.search('\/B[A-Z0-9]{9}', new).group(0)
            prod_link_id =prod_link_id.replace("/", "")

            if prod_link_id not in prod_df['ProdID'] and bool(re.search('[A-Z]', prod_link_id)) == True:
                prod_temp['ProdID'].append(prod_link_id)
                prod_temp['Status'].append("Added")
            else: 
                print "invalid page"

        else: 
            continue 
    prod_df = prod_df.append(pd.DataFrame(prod_temp, columns=['ProdID', 'Status']), ignore_index=True)
    prod_df = prod_df.drop_duplicates()

def validate_prods():
    for index, row in prod_df.iterrows():
        if row["Status"] == "Added":
            prod_link = "https://www.amazon.com.mx/dp/" + row['ProdID'] + "/"
            driver.get(prod_link)
            html = driver.page_source 
            soup = BeautifulSoup(html, "lxml")
            try:
                cat_list = soup.find('ul', attrs={"class": "a-unordered-list a-horizontal a-size-small"})
                cats = cat_list.findAll('a')
                print "total cats" + str(len(cats))
                cat1 = cats[0].text
                cat2 = cats[1].text
                r = re.compile(r"^\s+", re.MULTILINE)
                cat1 = r.sub("", cat1)
                cat2 = r.sub("", cat2)
                print cat1, cat2
                prod_df.set_value(index, 'Category', cat1)
                prod_df.set_value(index, 'Sub', cat2)
            except Exception as e:
                print e
                print "no cats"
                prod_df.set_value(index, 'Category', "None")
                prod_df.set_value(index, 'Sub', "None")
                prod_df.set_value(index, 'Status', "Invalid")
            try:    
                title = soup.find('h1', attrs={"id": "title"})
                title = title.text
                title = r.sub("", title)
                print title 
                prod_df.set_value(index, 'Title', title)
                
    
            except Exception as e:
                print e
                print "no title"
                title = "None"
                prod_df.set_value(index, 'Title', title)
                prod_df.set_value(index, 'Status', "Invalid")
                continue 
            try:
                rev_text = soup.findAll('div',attrs={"class" : "a-row a-spacing-small"})
                numrevs = len(rev_text)
                print numrevs
                dupes = 0
                for rev in soup.findAll('div',attrs={"class" : "a-section celwidget"}):
                    review = rev.find('div',attrs={"class" : "a-section"})
                    review = review.text
                    if review in just_revs['Text']:
                        dupes += 1
                    else:
                        print "not dupe"
                prod_df.set_value(index, 'Duplicate', dupes)
    
            except Exception as e:
                print e
                print "no reviews"
        
            prod_df.set_value(index, 'Duplicate', 0)
        else:
            pass 

def check_similar_prods():
    for index, row in prod_df.iterrows():
        checker = row['ProdID']
#        others = prod_df.ProdID.loc[lambda s: s not in checker]
        others = prod_df.loc[lambda df: df.ProdID != checker]
        print others 
#        matches = process.extract(row['Title'], others['Title'], limit=10)
#        print matches 


fuzz.ratio()
    
def get_reviews(prod_id):
    global rev_df, linkdf
    data = {'ProdID':[], 'Link':[], 'Rating': [], 'Text':[]}
    prod_link = "https://www.amazon.com.mx/product-reviews/" + prod_id + "/"
    driver.get(prod_link)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    while soup.find('li', attrs={"class": "a-last"}):
        last = soup.find('li', attrs={"class": "a-last"})
        next_links = last.findChildren()
        the_link = next_links[0]
        try:
            the_link = the_link['href']
            
            prod_link = "https://www.amazon.com.mx" +the_link
            driver.get(prod_link)
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            if soup.find_all('div',attrs={"class" : "a-section celwidget"}):
                for review in soup.find_all('div',attrs={"class" : "a-section celwidget"}):
                    star = review.find('span',attrs={"class" : "a-icon-alt"})
                    star = re.search(r'[0-9].[0-9]', star.text).group(0)
    
                    rev_text = review.find('span',attrs={"class" : "a-size-base review-text"})
                    rev_text = rev_text.text
                    data['ProdID'].append(prod_id)
                    data['Link'].append("None")
                    data['Rating'].append(star)
                    data['Text'].append(rev_text)
                rev_df = rev_df.append(pd.DataFrame(data, columns=['ProdID', 'Link', 'Rating', 'Text']), ignore_index=True)
                rev_df =  rev_df.drop_duplicates()

            else: 
                "no reviews"
        except Exception:
            rev_df = rev_df.append(pd.DataFrame(data, columns=['ProdID', 'Link', 'Rating', 'Text']), ignore_index=True)
            rev_df =  rev_df.drop_duplicates()
            get_content()
            
            
    print "boo"
    rev_df = rev_df.append(pd.DataFrame(data, columns=['ProdID', 'Link', 'Rating', 'Text']), ignore_index=True)
    rev_df =  rev_df.drop_duplicates()
    get_content()
    

    
    try:
        for review in soup.find_all('div',attrs={"class" : "a-section celwidget"}):
            star = review.find('span',attrs={"class" : "a-icon-alt"})
            rev_text = review.find('span',attrs={"class" : "a-size-base review-text"})
            rev_text = rev_text.text
            data['ProdID'].append(prod_id)
            data['Link'].append("None")
            data['Rating'].append(star)
            data['Text'].append(rev_text)
            
        rev_df = rev_df.append(pd.DataFrame(data, columns=['ProdID', 'Link', 'Rating', 'Text']), ignore_index=True)
        rev_df =  rev_df.drop_duplicates()
    except Exception:
        print "hit a snag"
        rev_df = rev_df.append(pd.DataFrame(data, columns=['ProdID', 'Link', 'Rating', 'Text']), ignore_index=True)
        rev_df =  rev_df.drop_duplicates()
        
        get_content() 


run = 0 
def get_content():
    global run, rev_df 
    while run < 10:   
        print run 
        for index, row in prod_df.iterrows():
                if row["Status"] == "Added":
                    print "scraping a new one" 
                    wait_time = random.randint(1, 6)
                    time.sleep(wait_time)
                    prod_df.set_value(index, 'Status', "Scraped")
                    run += 1
                    amzn_scrape(row["ProdID"])   
                    get_reviews(row["ProdID"])
                    return prod_df, run
                else:
                    print "already scraped"
    print "dumping df"
    run = 0
    time.sleep(400)
    update_rev_db()
    rev_df = pd.DataFrame(columns=['ProdID', 'Link', 'Rating', 'Text'])
    get_content()
    
def update_rev_db():
    conn_string = "host='localhost' dbname='mexican_politics' user='presdb' password='dbpass'"
    print "Connecting to database\n	->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    for index, row in rev_df.iterrows():
        sql = "INSERT INTO amzn_revs(ProdID, Link, Rating, Text) VALUES(%s, %s, %s, %s)"
        data = (rev_df['ProdID'][index],  rev_df['Link'][index], rev_df['Rating'][index], rev_df['Text'][index])
        cursor.execute(sql, data)
        conn.commit()


def get_prod_list():
    conn_string = "host='localhost' dbname='mexican_politics' user='presdb' password='dbpass'"
    print "Connecting to database\n	->%s" % (conn_string)
     
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cursor.execute("SELECT prodID, status FROM prod_list")
    prod_list = cursor.fetchall()
    prod_list = pd.DataFrame(prod_list)
    prod_df = pd.DataFrame()
    prod_df = prod_df.append(prod_list)

    #prod_df = prod_df.rename(index=str, columns={0: "ProdID", 1: "Status"})
    return prod_df

def just_text():
    conn_string = "host='localhost' dbname='mexican_politics' user='presdb' password='dbpass'"
    print "Connecting to database\n	->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM amzn_revs")
    rev_list = cursor.fetchall()
    rev_list = pd.DataFrame(rev_list)
    just_revs = pd.DataFrame(columns=['Text'])
    just_revs = just_revs['Text'].append(rev_list)

    return just_revs

def update_prod_db():
    conn_string = "host='localhost' dbname='mexican_politics' user='presdb' password='dbpass'"
    print "Connecting to database\n	->%s" % (conn_string)
     
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    sql = "DELETE FROM prod_list"
    cursor.execute(sql)

    for index, row in prod_df.iterrows():

        sql = "INSERT INTO prod_list(prodID, status) VALUES(%s, %s)"
        data = (prod_df['ProdID'][index],  prod_df['Status'][index])
        cursor.execute(sql, data)
        conn.commit()

just_revs = just_text()
just_revs = just_revs.rename(index=str, columns={0:"Text"})
prod_df = get_prod_list()
prod_df = prod_df.rename(index=str, columns={0: "ProdID", 1: "Status", })
validate_prods()

#amzn_scrape("B013VJPU10")
#get_reviews("B010U3XO3Q")
#new_df = rev_df  
#rev_df = new_df
#new_prod = prod_df
#get_prod_list()
#get_content()