# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 18:06:16 2017

@author: spnichol
"""

	

import psycopg2
import sys
 
def main():
	#Define our connection string
	conn_string = "host='localhost' dbname='mexican_politics' user='presdb' password='dbpass'"
 
	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)
 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	print "Connected!\n"
 
if __name__ == "__main__":
	main()

for item in items:
    city = item[0]
    price = item[1]
    info = item[2]

    query =  "INSERT INTO items (info, city, price) VALUES (%s, %s, %s);"
    data = (info, city, price)

    cursor.execute(query, data)
    conn.commit()
    
