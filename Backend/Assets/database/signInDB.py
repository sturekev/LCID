# this folder will process db connection, have function allow to connect to db
from Backend.Assets.database.db_config import get_db_info
import psycopg2
from psycopg2 import *

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

