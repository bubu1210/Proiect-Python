import logging

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="storage"
)

# print(mydb)

# mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE storage")


''' mycursor.execute(" CREATE TABLE songs "
                 "(id int NOT NULL AUTO_INCREMENT,"
                 "file_name varchar(100) NOT NULL,"
                 "artist_name varchar(100) NOT NULL,"
                 "song_name varchar(100) NOT NULL,"
                 "release_date date NOT NULL,"
                 "extension_type varchar(10) NOT NULL,"
                 "tag_list varchar(100) NOT NULL,"
                 "PRIMARY KEY(id))")
'''

