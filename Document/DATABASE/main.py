import psycopg2
from psycopg2 import OperationalError
from db_config import get_db_info


filename='db_info.ini'
section='postgres-sample-db'
db_info = get_db_info(filename,section)

db_connection = None
try:
    db_connection = psycopg2.connect(**db_info)
    print("Successfully connected to the database.")

    db_cursor = db_connection.cursor()
    create_table = '''CREATE TABLE GuestAccount(
                          id SERIAL PRIMARY KEY,
                          username varchar(50),
                          password varchar(50),
                          userToken varchar(50),
                          tokenExpiration DATE);'''
    db_cursor.execute(create_table)
    create_table = '''CREATE TABLE Account(
                          accountId SERIAL PRIMARY KEY,
                          jpeg varchar(50),
                          resident varchar(50),
                          residentToken varchar(50),
                          hallToken varchar(50),
                          tokenExpiration DATE);'''
    db_cursor.execute(create_table)

except OperationalError:
    print("Error connecting to the database :/")

finally:
    if db_connection:
        db_connection.close()
        print("Closed connection.")