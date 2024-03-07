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
    db_cursor.execute('''SELECT fullname, username, password, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    info_result = db_cursor.fetchall()
    print(info_result)

except OperationalError:
    print("Error retrieving data :/")
    print(OperationalError)

finally:
    if db_connection:
        db_connection.close()
        print("Closed connection.")