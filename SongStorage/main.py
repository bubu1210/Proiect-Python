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


