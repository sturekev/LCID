# this folder will process db connection, have function allow to connect to db
import psycopg2
from psycopg2 import *


from configparser import ConfigParser

def get_db_info(filename, section):
    # instantiating the parser object
    parser=ConfigParser()
    parser.read(filename)

    db_info={}
    if parser.has_section(section):
         # items() method returns (key,value) tuples
         key_val_tuple = parser.items(section) 
         for item in key_val_tuple:
             db_info[item[0]]=item[1] # index 0: key & index 1: value

    return db_info
# Connection parameters
def getAccountPass(username):
    try :
        filename='db_info.ini'
        section='cardReaderDB'
        db_info = get_db_info(filename, section)

        db_connection = psycopg2.connect(**db_info)
        cur = db_connection.cursor()
        sql_query = f"SELECT password FROM guest_account WHERE username = '{username}';"
        cur.execute(sql_query)
        row = cur.ferchall()
        cur.close()
        return row
    except DataError:
        return "Error connecting to the database :/"

    finally:
        if db_connection:
            db_connection.close()
            return "Closed connection."

