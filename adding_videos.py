# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 20:16:38 2017

@author: spnichol
"""

from subprocess import Popen, PIPE
import pandas as pd
import re
import psycopg2

next_tok = 0
#df = pd.DataFrame(columns=['youID', 'pubdate', 'title','chanid', 'lat', 'lon', 'query', 'geoquery','radius'])



def vid_search(keyword, geo, rad):
    global next_tok,  df
    output = Popen(['python', 'video_search.py', '--q', keyword, '--location', geo, '--location-radius', rad, '--max-results', '50'], stdout=PIPE)
    videos = output.stdout.read()
    video_list = re.findall('\[.*?\]',videos)
    next_tok = re.search('token(.*):', videos).group(0)
    next_tok = next_tok.replace("token: ", "")
    next_tok = next_tok.replace(" :", "")
    

    for vid in video_list:
        data = {'youID': [], 'pubdate':[], 'title':[], 'chanid':[], 'lat':[], 'lon':[], 'query':[], 'geoquery':[], 'radius':[]}

        if vid in df["youID"]:
            pass
        else:
            print vid
            try:
                regex = re.compile(r'TITLE:(.*)DATE :')
                title = regex.search(vid).group(0)
                title =title.replace('TITLE:', '')
                continue 
            except: 
                print "no title" 
                date = "None"
            
            try: 
                date = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}', vid).group(0)
                continue 
            except: 
                print "no date" 
                date = "None"
            try: 
                vidid = re.search('VIDID:(.*)]', vid).group(0)
                vidid = vidid.replace('VIDID:', '')
                vidid= vidid.replace(']', '')
            except: 
                print "no vidid" 
                vidid = "None"
            try: 
                chanid = re.search("CHANID:(.*) V", vid).group(0)
                chanid = chanid.replace("V", "")
            except: 
                print "no chan id" 
                chanid = "None"

            try: 
                lat = re.search('LAT: (.*) LONG', vid).group(0)
                lat = lat.replace(" LONG", "")
                lon = re.search('LONG : (.*)]', vid).group(0)
                lon = lon.replace("]", "")
            except: 
                print "no lat lon" 
                lat = "None"
                lon = "None"
        data['chanid'].append(chanid)
        data['lat'].append(lat)
        data['lon'].append(lon)
        data["youID"].append(vidid)
        data["pubdate"].append(date)
        data["title"].append(title)
        data["query"].append(keyword)
        data["geoquery"].append(geo)
        data["radius"].append(rad)                 
        df = df.append(pd.DataFrame(data, columns=['youID', 'pubdate', 'title', 'chanid', 'lat', 'lon', 'query', 'geoquery', 'radius']), ignore_index=True)

def next_vids(keyword, new_tok, geo, rad):
    print "second round"
    global next_tok, df
    data = {'youID': [], 'pubdate':[], 'title':[], 'chanid':[], 'lat':[], 'lon':[], 'query':[], 'geoquery':[], 'radius':[]}

    output = Popen(['python', 'video_search.py', '--q', keyword, '--page-token', new_tok,'--location', geo, '--location-radius', rad], stdout=PIPE)
    videos = output.stdout.read()
    print videos 
    video_list = re.findall('\[.*?\]',videos)
    next_tok = re.search('token(.*):', videos).group(0)
    next_tok = next_tok.replace("token: ", "")
    next_tok = next_tok.replace(" :", "")
    for vid in video_list:
        if vid in df["youID"]:
            pass
        else:
            print "confirmed"
            try:
                regex = re.compile(r'TITLE:(.*)DATE :')
                title = regex.search(vid).group(0)
                title =title.replace('TITLE:', '')
            except: 
                print "no title" 
            
            try: 
                date = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}', vid).group(0)
            except: 
                print "no date" 
            try: 
                vidid = re.search('VIDID:(.*) L', vid).group(0)
                vidid = vidid.replace('VIDID:', '')
                vidid= vidid.replace('L', '')
            except: 
                print "no vidid" 
            try: 
                chanid = re.search("CHANID:(.*) V", vid).group(0)
                chanid = chanid.replace("CHANID: ", "")
                chanid = chanid.replace("V", "")
            except: 
                print "no chan id" 
                chanid = "None"
                
            try: 
                lat = re.search('LAT: (.*) LONG', vid).group(0)
                lat = lat.replace("LAT: ", "")
                lat = lat.replace(" LONG", "")
                lon = re.search('LONG : (.*)]', vid).group(0)
                lon = lon.replace("LONG : ", "")
                lon = lon.replace("]", "")
            except: 
                print "no lat lon" 
            data['chanid'].append(chanid)
            data['lat'].append(lat)
            data['lon'].append(lon)
            data["youID"].append(vidid)
            data["pubdate"].append(date)
            data["title"].append(title)
            data["query"].append(keyword)
            data["geoquery"].append(geo)
            data["radius"].append(rad)
        df = df.append(pd.DataFrame(data, columns=['youID', 'pubdate', 'title', 'chanid', 'lat', 'lon', 'query', 'geoquery', 'radius']), ignore_index=True)

      


def search_by_loc(keyword, loc, rad):
    
    output = Popen(['python', 'loc_search.py', '--q', keyword, '--location', loc, '--location-radius', rad, '--max-results', '50'], stdout=PIPE)
    videos = output.stdout.read()
    print videos 
    
def search_by_loc2(keyword):
    
    output = Popen(['python', 'loc_search.py', '--q', keyword, '--max-results', '50'], stdout=PIPE)
    videos = output.stdout.read()
    print videos 

        

def add_to_DB():
    conn_string = "host='192.168.1.2' dbname='mexican_politics' user='presdb' password='dbpass'"
    print "Connecting to database\n	->%s" % (conn_string)
     
    conn = psycopg2.connect(conn_string)
     
    cursor = conn.cursor()
    
    for index, row in df.iterrows():
        sql = "INSERT INTO vid_list(youID, title, pubdate, query, chanid, lat, lon, geoquery, radius) VALUES(%s, %s, %s, %s, %s, %s, %s,%s , %s)"
        data = (df['youID'][index],  df['title'][index], df['pubdate'][index], df['query'][index], df['chanid'][index], df['lat'][index], df['lon'][index], df['geoquery'][index], df['radius'][index])
        cursor.execute(sql, data)
        conn.commit()

def term_search(term, geo, rad):
    vid_search(term, geo, rad)
    
    try:
        
        while len(df) < 10000000:
                next_vids(term, next_tok, geo, rad)
    except Exception as e:
        print e
        if "AttributeError: 'NoneType' object has no attribute 'group'" in str(e):
            print 'not found'
            pass 

term_list = ["EEUU", "EU", "Gringolandia", "Trump", "Pena Nieto", "EPN", "AMLO", "Lopez Obrador", "Morena", "PRI", "PAN", "gasolinazo", "gringo"]
for term in term_list:
    term_search(term,"19.453342, -99.129892", "900km")
    add_to_DB()
    
#term_search("amlo", "23.850936, -101.264416", "500km")
#add_to_DB()