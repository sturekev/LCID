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



def create_mockdata(db_connection):
    
    db_cursor = db_connection.cursor()
    # Generate random data and insert it into the guest_account table
    num_of_users = 10  # can change this depends on how many random datapoints needed
    file = open("mockdata.txt", "w")
    file.write("username\t")
    file.write("passwordStr\t")
    file.write("passwordHashed\t")
    file.write("pubKey\t")
    file.write("user_token\t")
    file.write("token_expiration\n")

    for _ in range(num_of_users):
        username = generate_random_string(8)  # assuming 8-character usernames
        password = generate_random_string(10)  # assuming 10-character passwords
        hashedPass = hashedPassword(encodePassword(password)) # generate password with 
        pubKey ,user_token = ExportNewRSAKey()  # 20-character user token
        token_expiration = '2024-12-31'  # sample expiration date, you can randomize this too

        db_cursor = db_connection.cursor()
        db_cursor.execute("INSERT INTO guest_account(username, password, user_token, token_expiration) VALUES (%s, %s, %s, %s);",
                            (username, hashedPass , user_token, token_expiration))
        db_connection.commit()
        file.write(username +"\t")
        file.write(password +"\t")
        file.write(str(hashedPass, encoding='utf-8') +"\t")
        file.write(str(pubKey, encoding='utf-8') +"\t")
        file.write(str(user_token, encoding='utf-8') +"\t")
        file.write(token_expiration +"\n")
    return db_connection
    