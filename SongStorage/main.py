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


def modify_data():
    id_to_be_modified = input("Song to be modified: ")
    modify_file_name = input("Modify file name: ")
    modify_artist_name = input("Modify artist name: ")
    modify_song_name = input("Modify song name: ")
    modify_release_date = input("Modify release date: ")
    modify_extension_type = input("Modify extension type: ")
    modify_tag_list = input("Modify tag list: ")

    # Creating a cursor object using the cursor() method
    mycursor = mydb.cursor()

    try:
        if len(modify_file_name) != 0:
            stmt1 = "UPDATE SONGS SET file_name = %s WHERE ID = %s "
            data1 = (modify_file_name, id_to_be_modified)
            mycursor.execute(stmt1, data1)
            mydb.commit()
            print("File name modified")
        if len(modify_artist_name) != 0:
            stmt2 = "UPDATE SONGS SET artist_name = %s WHERE ID = %s "
            data2 = (modify_artist_name, id_to_be_modified)
            mycursor.execute(stmt2, data2)
            mydb.commit()
            print("Artist name modified")
        if len(modify_song_name) != 0:
            stmt3 = "UPDATE SONGS SET song_name = %s WHERE ID = %s "
            data3 = (modify_song_name, id_to_be_modified)
            mycursor.execute(stmt3, data3)
            mydb.commit()
            print("Song name modified")
        if len(modify_release_date) != 0:
            stmt4 = "UPDATE SONGS SET release_date = %s WHERE ID = %s "
            data4 = (modify_release_date, id_to_be_modified)
            mycursor.execute(stmt4, data4)
            mydb.commit()
            print("Release date modified")
        if len(modify_extension_type) != 0:
            stmt5 = "UPDATE SONGS SET extension_type = %s WHERE ID = %s "
            data5 = (modify_extension_type, id_to_be_modified)
            mycursor.execute(stmt5, data5)
            mydb.commit()
            print("Extension type modified")
        if len(modify_tag_list) != 0:
            stmt6 = "UPDATE SONGS SET tag_list = %s WHERE ID = %s "
            data6 = (modify_tag_list, id_to_be_modified)
            mycursor.execute(stmt6, data6)
            mydb.commit()
            print("Tag list modified")

    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))
        mycursor.close()
        logging.exception(error)


def search_song():
    print("List of criteria: artist_name, song_name, extension_type")
    column1 = input("column1: ")
    criteria1 = input("criteria1: ")
    column2 = input("column2: ")
    criteria2 = input("criteria2: ")

    mycursor = mydb.cursor()
    try:
        stmt2 = """select * from songs where %s ='%s' and %s ='%s' """ % (column1, criteria1, column2, criteria2)
        mycursor.execute(stmt2)
        records = mycursor.fetchall()
        print("Total number of results is: ", mycursor.rowcount)

        print("\nPrinting each result")
        for row in records:
            print("ID = ", row[0], )
            print("File Name = ", row[1])
            print("Artist name = ", row[2])
            print("Song name  = ", row[3]),
            print("Release date  = ", row[4]),
            print("Extension type  = ", row[5]),
            print("Tag list  = ", row[6])

    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))
        mycursor.close()
        logging.exception(error)


def create_save_list():
    print("List of criteria for the zip: artist_name, song_name, extension_type")
    column1 = input("column1: ")
    criteria1 = input("criteria1: ")
    column2 = input("column2: ")
    criteria2 = input("criteria2: ")

    mycursor = mydb.cursor()
    try:
        stmt2 = """select * from songs where %s ='%s' and %s ='%s' """ % (column1, criteria1, column2, criteria2)
        mycursor.execute(stmt2)
        records = mycursor.fetchall()
        print("Total number of results is: ", mycursor.rowcount)

        print("\nPrinting each result")

        def return_files(response):
            files = []
            for row in response:
                print("File Name = ", row[1])
                rand =''.join(row[1]) + "." + ''.join(row[5])
                files.append(rand)
                source = "C:/Users/bubux/PycharmProjects/SongStorage/Storage/"
                with zipfile.ZipFile(source+rand + ".zip", "w", zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.write(source+rand)

            return files

        create_directory("zipfolder")
        source = "C:/Users/bubux/PycharmProjects/SongStorage/Storage"
        destination = "C:/Users/bubux/PycharmProjects/SongStorage/zipfolder"
        files = return_files(records)


    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))
        mycursor.close()
        logging.exception(error)

