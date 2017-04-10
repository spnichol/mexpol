# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 10:06:04 2017

@author: spnichol
"""
import psycopg2
conn_string = "host='justnew.cl95re7xujec.us-east-1.rds.amazonaws.com' dbname='postgres' user='pres' password='marigold'"
print "Connecting to database\n	->%s" % (conn_string)
 
conn = psycopg2.connect(conn_string)
 
cursor = conn.cursor()
vid_list = "CREATE TABLE current_videos(youid varchar(25), pubdate date, title varchar(500), query varchar(500), chanid varchar(200), lat varchar(100), lon varchar(100), geoquery varchar(200), radius varchar(200) );"
cursor.execute(vid_list)


comm_list = "CREATE TABLE vid_comments (youid varchar(25), pubdate date, content varchar(1000000));"
cursor.execute(comm_list)
conn.commit()

delete_table = "DROP TABLE new_vid_list;"
cursor.execute(delete_table)
conn.commit()
conn.close()

delete_tbl_data = "DELETE FROM vid_comments;"
rb = "ROLLBACK;"
cursor.execute(rb)
cursor.execute(delete_tbl_data)

