# this folder will process db connection, have function allow to connect to db
from db_config import get_db_info
import psycopg2
from psycopg2 import OperationalError

# Connection parameters
def connDb():
    try :
        filename='db_info.ini'
        section='cardReaderDB'
        db_info = get_db_info(filename, section)

        db_connection = psycopg2.connect(**db_info)
        return db_connection
    except OperationalError:
        return "Error connecting to the database :/"

    finally:
        if db_connection:
            db_connection.close()
            return "Closed connection."

