import psycopg2
from psycopg2 import OperationalError
from db_config import get_db_info

from mockdata.mockdata import *
filename='db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)

db_connection = None

db_connection = psycopg2.connect(**db_info)
print("Successfully connected to the database.")

    # db_cursor = db_connection.cursor()
    # create_table = '''DROP TABLE IF EXISTS account CASCADE;
    #                     CREATE TABLE account(
    #                     id SERIAL PRIMARY KEY,
    #                     fullname varchar(255) NOT NULL,
    #                     username varchar(255) NOT NULL,
    #                     password varchar(255) NOT NULL);'''
    # db_cursor.execute(create_table)

    # db_connection = create_mockdata_account(db_connection)
    # print("Records inserted successfully to account table")
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS building_info CASCADE;
    #                     CREATE TABLE building_info(
    #                     building_id SERIAL PRIMARY KEY,
    #                     building_name varchar(255) UNIQUE NOT NULL);'''
    # db_cursor.execute(create_table)

    # db_connection = create_mockdata_building_info(db_connection)
    # print("Records inserted successfully to building info table")
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS account_profile CASCADE;
    #                     CREATE TABLE account_profile(
    #                     id_number varchar(255) PRIMARY KEY,
    #                     account_id INTEGER NOT NULL,
    #                     user_token BYTEA NOT NULL,
    #                     housing INTEGER NOT NULL,
    #                     FOREIGN KEY(account_id) REFERENCES account(id),
    #                     FOREIGN KEY(housing) REFERENCES building_info(building_id));'''
    # db_cursor.execute(create_table)

    # db_connection = create_mockdata_account_profile(db_connection)
    # print("Records inserted successfully to account profile info table")
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS meal_balance CASCADE;
    #                     CREATE TABLE meal_balance(
    #                     account_id INTEGER NOT NULL,
    #                     role varchar(255) NOT NULL,
    #                     swipes_remaining INTEGER NOT NULL,
    #                     dining_dollars FLOAT4 NOT NULL,
    #                     meal_plan varchar(255) NOT NULL,
    #                     FOREIGN KEY(account_id) REFERENCES account(id));'''
    # db_cursor.execute(create_table)

    # db_connection = create_mockdata_meal_balance(db_connection)
    # print("Records inserted successfully to meal balance table")
    # db_connection.commit()

print("\nRetrieval from database imminent...")

db_cursor = db_connection.cursor()
db_cursor.execute('''SELECT fullname, username, password, id_number, building_name 
                    FROM account, account_profile, building_info 
                    WHERE account_profile.account_id = account.id 
                    AND building_info.building_id = account_profile.housing''')
info_result = db_cursor.fetchall()
print(info_result)

db_connection.close()
print("Closed connection.")
        