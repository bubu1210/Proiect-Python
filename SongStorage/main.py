# Import logging module
import logging
import logging.config
import os
import shutil
import sys
import mysql.connector
import zipfile
from playsound import playsound

# Set the log filename
filename = 'my.log'

# Set the log filename and level
logging.basicConfig(filename=filename, level=logging.DEBUG)

# Print messages to the file
logging.debug('Debug message')
logging.info('Info message')
logging.error('Error Message')


def create_directory(name):
    # Directory
    directory = name

    # Parent Directory path
    parent_dir = "C:/Users/bubux/PycharmProjects/SongStorage/"

    # Path
    path = os.path.join(parent_dir, directory)

    # Create the directory
    try:
        os.mkdir(path, mode=0o777,dir_fd=None)
        print("Directory '% s' created" % directory)
    except OSError as error:
        print(error)
        logging.exception(error)
        logging.info("Folderul a fost deja creat")


create_directory("Storage")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="storage"
)

destination = "C:/Users/bubux/PycharmProjects/SongStorage/Storage"  # Destination directory


def add_song():
    file_name = input("File name: ")
    artist_name = input("Artist name: ")
    song_name = input("Song name: ")
    release_date = input("Release date: ")
    extension_type = input("Extension type: ")
    tag_list = input("Tag list: ")
    source = "C:/Users/bubux/PycharmProjects/SongStorage/Music" + file_name + "." + extension_type

    # Copy file to Storage
    try:
        shutil.copy2(source, destination)
        print("File copied")
    except shutil.Error as error:
        print(error)
        logging.exception(error)

    # Creating a cursor object using the cursor() method
    mycursor = mydb.cursor()

    # Preparing SQL query to INSERT a record into the database.
    insert_stmt = (
        "INSERT INTO SONGS(FILE_NAME, ARTIST_NAME, SONG_NAME, RELEASE_DATE, EXTENSION_TYPE, TAG_LIST)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    data = (file_name, artist_name, song_name, release_date, extension_type, tag_list)

    try:
        # Executing the SQL command
        mycursor.execute(insert_stmt, data)

        # Commit your changes in the database
        mydb.commit()

        # Get Inserted ID
        print("ID: ", mycursor.lastrowid)

    except:
        # Rolling back in case of error
        mydb.rollback()
        mycursor.close()


def delete_song():
    id_to_be_deleted = input("ID to be deleted: ")
    mycursor = mydb.cursor()
    try:
        stmt1 = "SELECT file_name, extension_type FROM songs WHERE ID = " + id_to_be_deleted
        mycursor.execute(stmt1)
        myresult = mycursor.fetchall()
        for row in myresult:
            song_to_be_deleted = row[0] + "." + row[1]
            print(song_to_be_deleted)
            to_be_deleted = destination + song_to_be_deleted
            try:
                if os.path.exists(to_be_deleted):
                    os.remove(to_be_deleted)
                    print("File deleted")
                else:
                    print("The file does not exist")
            except OSError as e:
                print("Error: %s : %s" % (to_be_deleted, e.strerror))
                logging.exception(e)

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        logging.exception(e)

    try:
        stmt2 = "DELETE from songs where id = " + id_to_be_deleted
        mycursor.execute(stmt2)
        mydb.commit()
        print("Song removed from database")
    except mysql.connector.Error as error:
        print("Failed to delete record from table: {}".format(error))
        mycursor.close()
        logging.exception(error)


