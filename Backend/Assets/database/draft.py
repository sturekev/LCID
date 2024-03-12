from db_config import get_db_info

import psycopg2
from psycopg2 import OperationalError

filename='Assets/database/db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)




def get_user_caf_db (stdid):
    caf_db = {}
    db_connection = psycopg2.connect(**db_info)

    db_cursor = db_connection.cursor()
    db_cursor.execute("""SELECT id_number , role, 
                        swipes_remaining, dining_dollars
                        FROM account_profile, meal_balance
                        WHERE meal_balance.account_id = account_profile.account_id 
                        AND account_profile.id_number = (%s)""", (stdid,))
    info_result = db_cursor.fetchall()
    for entry in info_result:
        caf_db[entry[0]] = {
            "student_id" : entry[0],
            "swipes" : entry[2],
            "dining_dolars" : entry[3],
            "role" : entry[1]
        }

    return caf_db

print(get_user_caf_db('529194'))
# print(get_user_caf_db())