import psycopg2
from psycopg2 import OperationalError
from db_config import get_db_info


filename='db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)

db_connection = None
try:
    db_connection = psycopg2.connect(**db_info)
    print("Successfully connected to the database.")

    db_cursor = db_connection.cursor()
    create_table = '''DROP TABLE IF EXISTS guest_account;
                        CREATE TABLE guest_account(
                        id SERIAL PRIMARY KEY,
                        username varchar(50) NOT NULL,
                        password varchar(50) NOT NULL,
                        user_token varchar(50)NOT NULL,
                        token_expiration DATE NOT NULL);'''
    db_cursor.execute(create_table)
    db_connection.commit()

    create_table = '''DROP TABLE IF EXISTS account;
                        CREATE TABLE account(
                        account_id SERIAL PRIMARY KEY,
                        jpeg varchar(50) NOT NULL,
                        resident varchar(50) NOT NULL,
                        resident_token varchar(50) NOT NULL,
                        hall_token varchar(50) NOT NULL,
                        token_expiration DATE NOT NULL);'''
    db_cursor.execute(create_table)
    db_connection.commit()

    create_table = '''DROP TABLE IF EXISTS building_info;
                        CREATE TABLE building_info(
                        building_id SERIAL PRIMARY KEY,
                        building_name varchar(50) NOT NULL,
                        resident_private_key varchar(50) NOT NULL,
                        hall_private_key varchar(50) NOT NULL,
                        expiration_date DATE NOT NULL);'''
    db_cursor.execute(create_table)
    db_connection.commit()

    # Changed student_id to account_id, 
    # because staff and faculty should also be in the building log, 
    # not just students
    create_table = '''DROP TABLE IF EXISTS building_log;
                        CREATE TABLE building_log(
                        account_id SERIAL PRIMARY KEY,
                        building_name varchar(50) NOT NULL,
                        acception BOOLEAN NOT NULL,
                        timestamp varchar(50) NOT NULL);'''
    db_cursor.execute(create_table)
    db_connection.commit()

    # # Changed student_id to account_id, 
    # # because staff and faculty can check out items,
    # # not just students
    # create_table = '''DROP TABLE IF EXISTS library_log;
    #                     CREATE TABLE library_log(
    #                     account_id SERIAL PRIMARY KEY,
    #                     lib_token varchar(50) NOT NULL,
    #                     building_token varchar(50) NOT NULL,
    #                     timestamp varchar(50) NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS dining_services;
                        # CREATE TABLE dining_services(
                        # id SERIAL PRIMARY KEY,
                        # name varchar(50) NOT NULL,
                        # resident_private_key varchar(50) NOT NULL,
                        # hall_private_key varchar(50) NOT NULL
                        # expiration_date DATE NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS lib_asset;
    #                     CREATE TABLE dining_services(
    #                     id SERIAL PRIMARY KEY,
    #                     name varchar(50) NOT NULL,
    #                     resident_private_key varchar(50) NOT NULL,
    #                     hall_private_key varchar(50) NOT NULL
    #                     expiration_date DATE NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

except OperationalError:
    print("Error connecting to the database :/")

finally:
    if db_connection:
        db_connection.close()
        print("Closed connection.")