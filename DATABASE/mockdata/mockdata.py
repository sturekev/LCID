# for generating random database
import bcrypt
import random
import string
import csv
from mockdata.hash import *

import psycopg2
from psycopg2 import OperationalError


def generate_random_string(length):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))



def create_mockdata_account(db_connection=None):
    
    db_cursor = db_connection.cursor()
    # Generate random data and insert it into the guest_account table
    num_of_users = 3  # can change this depends on how many random datapoints needed
    file = open("mockdata.txt", "w")
    file.write("username\t")
    file.write("passwordStr\t")
    file.write("passwordHashed\t")
    for _ in range(num_of_users):
        username = generate_random_string(8)  # assuming 8-character usernames
        password = generate_random_string(10)  # assuming 10-character passwords
        hashedPass = hashedPassword(encodePassword(password)) # generate password with 

        db_cursor = db_connection.cursor()
        db_cursor.execute("INSERT INTO guest_account(username, password) VALUES (%s, %s,);",
                            (username, hashedPass))
        db_connection.commit()
        file.write(username +"\t")
        file.write(password +"\t")
        file.write(str(hashedPass, encoding='utf-8') +"\t")
    return db_connection
    