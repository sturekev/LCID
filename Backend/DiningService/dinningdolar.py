import sys
from Assets.database.db_config import get_db_info

import psycopg2
from psycopg2 import OperationalError

filename='Assets/database/db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)




def get_user_caf_db ():
    users_db = {}
    db_connection = psycopg2.connect(**db_info)

    db_cursor = db_connection.cursor()
    db_cursor.execute('''SELECT username, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    info_result = db_cursor.fetchall()
    for entry in info_result:
        users_db[entry[1]] = {
            "username": entry[0],
            "email": f"{entry[0]}@luther.edu",
            "student_id": entry[1],
            "building": entry[2]
        }

    return users_db
