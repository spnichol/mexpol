# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:03:44 2017

@author: spnichol
"""


from subprocess import Popen, PIPE
import pandas as pd
import re
import psycopg2
import sys
import pprint

conn_string = "host='localhost' dbname='mexican_politics' user='presdb' password='dbpass'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()


def grab_comments(youID, next_tok, page_count):
    global comm_batch, data
    if page_count == 1:
        output = Popen(['python', 'comments.py', '--videoid', youID], stdout=PIPE)
    else:
        output = Popen(['python', 'comments.py', '--videoid', youID, '--pagetoken', next_tok], stdout=PIPE)
    page_count +=1
    comments  = output.stdout.read()
    try: 
        next_tok = re.search('token:(.*):', comments).group(0)
        next_tok = next_tok.replace("token: ", "")
        print "found token" 
    except Exception as e: 
        pass  
    try:
        comment_list = re.findall('\[.*?\]',comments)
        content = re.search('Content:(.*)]', comments).group(0)
        data = {'youID': [], 'pubdate':[], 'content':[]}
        for comment in comment_list:
            youID = youID
            try:
                pubdate = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}', comment).group(0)
            except Exception as e: 
                print e
                continue 
            try: 
                content = re.search('Content:(.*)]', comment).group(0)
                content = content.replace("Content: ", "")
                content = content.replace("]", "")
                data["youID"] = youID
                data["pubdate"] = pubdate
                data["content"]= content
            except Exception as e:
                print "issue" 
        try:
            comm_batch = data.values()
            comm_batch = list(comm_batch)
            comm_batch = tuple(comm_batch)
            sql = "INSERT INTO vid_comments (content, pubdate, youid)VALUES(%s, %s, %s)"
            cursor.execute(sql, comm_batch)
            conn.commit()
            print "comms added to db!"
        except Exception as e:
            print e
            print "DB Error"
        while next_tok != "first":
            print "scrapping next page" 
            grab_comments(youID, next_tok, page_count) 
    except Exception as e:
         print "skipping" 
         pass
        
def check_comments_db():
    global comments_list
    conn_string = "host='localhost' dbname='mexican_politics' user='presdb' password='dbpass'"
    print "Connecting to database\n	->%s" % (conn_string)
     
    conn = psycopg2.connect(conn_string)
     
    cursor = conn.cursor()
    cursor.execute("SELECT youid FROM vid_comments")
    comments_list = cursor.fetchall()

    comments_list = list(comments_list)
    comments_list = [t[0] for t in comments_list]
    comments_list = list(set(comments_list))
    return comments_list

def comment_iter():
    global vid_list
    conn_string = "host='localhost' dbname='mexican_politics' user='presdb' password='dbpass'   "
    print "Connecting to database\n	->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT youid FROM vid_list")
    vid_list = cursor.fetchall()
    vid_list = list(vid_list)
    vid_list= [t[0] for t in vid_list]
    vid_list = list(set(vid_list))
    for youID in vid_list: 
        youID = str(youID)
        youID = youID.replace(",", "")
        youID = youID.replace(")", "")
        youID = youID.replace("(", "")
        youID = youID.replace("'", "")
        youID = youID.replace("L", "")
    vid_list = pd.DataFrame(vid_list)
    return vid_list

def download_comments():
    numdl = 0
    for index, row in vid_df.iterrows():
        print row["youID"]
        if row["Status"] == "No_Added" and row["youID"] not in comments_list:   
            print "adding"
            vid_df.set_value(index, 'Status', "Downloaded")
            numdl += 1
            print numdl
            try:
                next_tok = "first"
                page_count = 1
                grab_comments(row["youID"], next_tok, page_count)
            except Exception as e:
                if "AttributeError: 'NoneType' object has no attribute 'group'" in str(e):
                    print 'no more comments'
                    vid_df.set_value(index, 'Status', "Downloaded")

        elif row["youID"] in comments_list:
            print "the comments have already been saved"
            
        else:
            pass
        
vid_df = comment_iter()
vid_df['Status'] = "No_Added" 
vid_df = vid_df.rename(index=str, columns={0:"youID", 1: "Status"})
download_comments()

