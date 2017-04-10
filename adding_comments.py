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

conn_string = "host='justnew.cl95re7xujec.us-east-1.rds.amazonaws.com' dbname='postgres' user='pres' password='marigold'"
print "Connecting to database\n	->%s" % (conn_string)   
conn = psycopg2.connect(conn_string)
     
cursor = conn.cursor()

next_tok = "first"
page_count = 1
def grab_comments():
    page_count = 1
    comm_count = 0
    next_tok = "first"
    data_temp = {'youID': [], 'pubdate':[], 'content':[]}
    for index, row in vid_df.iterrows():
        print "scraped: " +str(comm_count)
        df_main = pd.DataFrame(columns=['youID', 'pubdate', 'content'])
        if page_count == 1 and row["Status"] == "No_Added" and row["youID"] not in comments_list:   
            output = Popen(['python', 'comments.py', '--videoid', row["youID"]], stdout=PIPE)
        elif page_count > 1 and row["Status"] == "No_Added":
            output = Popen(['python', 'comments.py', '--videoid', row["youID"], '--pagetoken', next_tok], stdout=PIPE)
        else: 
            continue  
        
        comments  = output.stdout.read()
        try: 
            next_tok = re.search('token:(.*):', comments).group(0)
            next_tok = next_tok.replace("token: ", "")
        except Exception as e: 
            print "no tokens"
        try:
            comment_list = re.findall('\[.*?\]',comments)
            content = re.search('Content:(.*)]', comments).group(0)
            print len(comment_list)
            for comment in comment_list:
                try:
                    pubdate = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}', comment).group(0)
                except Exception as e: 
                    print e
                    pass 
                try: 
                    content = re.search('Content:(.*)]', comment).group(0)
                    content = content.replace("Content: ", "")
                    content = content.replace("]", "")
                    data_temp["content"]= content
                    data_temp["pubdate"]= pubdate 
                    data_temp["youID"] = row["youID"]
                    df_main = df_main.append(pd.DataFrame(data_temp, columns=['youID', 'pubdate', 'content'], index=[0]))

                except Exception as e:
                    print e
        except Exception as e:
           row["Status"] = "No_Comments"
           continue  

        try:
            df_2 = df_main.values

            comm_count = comm_count + len(df_2)
            dataText = ','.join(cursor.mogrify('(%s,%s,%s)', row) for row in df_2)
            cursor.execute('insert into vid_comments values ' + dataText)            
            conn.commit()
            
        except Exception as e:
            print e
            print "DB Error"
            
        if next_tok != "first":
            page_count += 1 
        else: 
            row["Status"] = "Downloaded"
            next_tok = "first"
        
def check_comments_db():
    global comments_list
    conn_string = "host='justnew.cl95re7xujec.us-east-1.rds.amazonaws.com' dbname='postgres' user='pres' password='marigold'"
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
    conn_string = "host='justnew.cl95re7xujec.us-east-1.rds.amazonaws.com' dbname='postgres' user='pres' password='marigold'"
    print "Connecting to database\n	->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT youid FROM current_videos")
    vid_list = cursor.fetchall()
    vid_list = list(vid_list)
    vid_list= [t[0] for t in vid_list]
    vid_list = pd.DataFrame(vid_list)
    return vid_list
    
vid_df = comment_iter()
comments_list = check_comments_db()
vid_df['Status'] = "No_Added" 
vid_df = vid_df.rename(index=str, columns={0:"youID", 1: "Status"})
grab_comments()


