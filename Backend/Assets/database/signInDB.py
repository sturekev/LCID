import psycopg2
from dbConnection import connDb
from psycopg2 import *

db_connection = connDb()

def getAccountPass (username, password):
    try: 
        
        cur = db_connection.cursor()
        sql_query = f"SELECT * WHERE username = {username};"
        cur.execute(sql_query)
        row = cur.ferchall()
        return row
    except DataError:
        return False
    finally:
        if db_connection:
            db_connection.close()
            return False

def updateUserToken (currUserToken):
    pass
cur = db_connection.cursor()

# Define your SQL query
sql_query = "SELECT * FROM your_table_name"

# Execute the query
cur.execute(sql_query)

# Fetch results
rows = cur.fetchall()

for row in rows:
    print(row)

# Close the cursor and connection
cur.close()
db_connection.close()