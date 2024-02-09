import psycopg2
from psycopg2 import OperationalError
from db_config import get_db_info

from mockdata.mockdata import *
filename='db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)

db_connection = None
try:
    db_connection = psycopg2.connect(**db_info)
    print("Successfully connected to the database.")

    db_cursor = db_connection.cursor()
    create_table = '''DROP TABLE IF EXISTS account CASCADE;
                        CREATE TABLE account(
                        id SERIAL PRIMARY KEY,
                        firstname varchar(255) NOT NULL,
                        lastname varchar(255),
                        username varchar(255) NOT NULL,
                        password BYTEA NOT NULL);'''
    db_cursor.execute(create_table)
    
    db_connection = create_mockdata_account(db_connection)
    print("Records inserted successfully to account table")
    db_connection.commit()

    create_table = '''DROP TABLE IF EXISTS building_info CASCADE;
                        CREATE TABLE building_info(
                        building_id SERIAL PRIMARY KEY,
                        building_name varchar(255) UNIQUE NOT NULL);'''
    db_cursor.execute(create_table)

    db_connection = create_mockdata_building_info(db_connection)
    print("Records inserted successfully to building info table")
    db_connection.commit()

    # Changed student_id to account_id, 
    # because staff and faculty should also be in the building log, 
    # not just students
    create_table = '''DROP TABLE IF EXISTS account_profile CASCADE;
                        CREATE TABLE account_profile(
                        id_number varchar(255) PRIMARY KEY,
                        account_id INTEGER NOT NULL,
                        user_token BYTEA NOT NULL,
                        housing INTEGER NOT NULL,
                        FOREIGN KEY(account_id) REFERENCES account(id),
                        FOREIGN KEY(housing) REFERENCES building_info(building_id));'''
    db_cursor.execute(create_table)
    
    db_connection = create_mockdata_account_profile(db_connection)
    print("Records inserted successfully to account profile info table")
    db_connection.commit()


    # create_table = '''DROP TABLE IF EXISTS building_log CASCADE;
    #                     CREATE TABLE building_log(
    #                     id SERIAL PRIMARY KEY,
    #                     account_id INTEGER REFERENCES account(id),
    #                     building_name varchar(255) REFERENCES building_info(building_name),
    #                     acception BOOLEAN NOT NULL,
    #                     timestamp TIME NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS library_log CASCADE;
    #                     CREATE TABLE library_log(
    #                     id SERIAL PRIMARY KEY,
    #                     account_id varchar(255) REFERENCES account(user_id),
    #                     lib_token varchar(255) NOT NULL,
    #                     building_token varchar(255) NOT NULL,
    #                     timestamp TIME NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS lib_asset CASCADE;
    #                     CREATE TABLE lib_asset(
    #                     id SERIAL PRIMARY KEY,
    #                     item_name varchar(255) NOT NULL,
    #                     type varchar(255) NOT NULL,
    #                     category varchar(255) NOT NULL,
    #                     quantity INTEGER NOT NULL,
    #                     available BOOLEAN NOT NULL,
    #                     expires DATE NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

#DECIDE MEAL PLAN LATER rework 
    # create_table = '''DROP TABLE IF EXISTS meal_balance CASCADE;
    #                     CREATE TABLE meal_balance(
    #                     account_id INTEGER NOT NULL,
    #                     name varchar(255) NOT NULL,
    #                     role varchar(255) NOT NULL,
    #                     swipes_remaining INTEGER NOT NULL,
    #                     dining_dollars FLOAT4 NOT NULL,
    #                     meal_plan varchar(255) NOT NULL,
    #                     expiration_date DATE NOT NULL,
    #                     FOREIGN KEY(account_id) REFERENCES account(id));'''
    create_table = '''DROP TABLE IF EXISTS meal_balance CASCADE;
                        CREATE TABLE meal_balance(
                        account_id INTEGER NOT NULL,
                        role varchar(255) NOT NULL,
                        swipes_remaining INTEGER NOT NULL,
                        dining_dollars FLOAT4 NOT NULL,
                        meal_plan varchar(255) NOT NULL,
                        FOREIGN KEY(account_id) REFERENCES account(id));'''
    db_cursor.execute(create_table)

    db_connection = create_mockdata_meal_balance(db_connection)
    print("Records inserted successfully to meal balance table")
    db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS dining_services CASCADE;
    #                     CREATE TABLE dining_services(
    #                     dining_services_id SERIAL PRIMARY KEY,
    #                     account_id varchar(255) REFERENCES account(user_id),
    #                     dining_service_name varchar(255) NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS cafeteria CASCADE;
    #                     CREATE TABLE cafeteria(
    #                     id INTEGER NOT NULL,
    #                     meal_time varchar(255) NOT NULL,
    #                     swipe INTEGER NOT NULL,
    #                     price FLOAT4 NOT NULL,
    #                     start_time TIME NOT NULL,
    #                     end_time TIME NOT NULL,
    #                     FOREIGN KEY(id) REFERENCES dining_services(dining_services_id));'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS martys CASCADE;
    #                     CREATE TABLE martys(
    #                     id INTEGER REFERENCES dining_services(dining_services_id),
    #                     price FLOAT4 NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS c_store CASCADE;
    #                     CREATE TABLE c_store(
    #                     id INTEGER REFERENCES dining_services(dining_services_id),
    #                     price FLOAT4 NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

    # create_table = '''DROP TABLE IF EXISTS nordic_brew CASCADE;
    #                     CREATE TABLE nordic_brew(
    #                     id INTEGER REFERENCES dining_services(dining_services_id),
    #                     price FLOAT4 NOT NULL);'''
    # db_cursor.execute(create_table)
    # db_connection.commit()

except OperationalError:
    print("Error connecting to the database :/")
    print(OperationalError)

finally:
    if db_connection:
        db_connection.close()
        print("Closed connection.")

try:
    db_connection = psycopg2.connect(**db_info)
    print("\nRetrieval from database imminent...")
    
    db_cursor = db_connection.cursor()
    db_cursor.execute('''SELECT firstname, lastname, username, password, id_number, building_name FROM account, account_profile, building_info WHERE account_profile.account_id = account.id AND building_info.building_id = account_profile.housing''')
    info_result = db_cursor.fetchall()
    print(info_result)

except OperationalError:
    print("Error retrieving data :/")
    print(OperationalError)

finally:
    if db_connection:
        db_connection.close()
        print("Closed connection.")

try:
    users_db = {}
    db_connection = psycopg2.connect(**db_info)
    db_cursor = db_connection.cursor()
    db_cursor.execute('''SELECT firstname, lastname, username, password, id_number, building_name FROM account, account_profile, building_info WHERE account_profile.account_id = account.id AND building_info.building_id = account_profile.housing''')
    info_result = db_cursor.fetchall()

    for entry in info_result:
        users_db[entry[2]] = {
            "username": entry[2],
            "full_name": f"{entry[0]} {entry[1]}",
            "email": f"{entry[2]}@luther.edu",
            "hashed_password": entry[3],
            "disabled": False,
            "student_id": entry[4],
            "building": entry[5]
        }
    
    for username, info in users_db.items():
        print(username, info)
        print("\n")
        
except OperationalError:
    print("Error connecting to the database :/")
    print(OperationalError)

finally:
    if db_connection:
        db_connection.close()
        print("Closed connection.")