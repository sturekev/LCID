from db_config import get_db_info

import psycopg2
from psycopg2 import OperationalError

filename='Assets/database/db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)




# def get_user_caf_db (stdid):
#     caf_db = {}
#     db_connection = psycopg2.connect(**db_info)

#     db_cursor = db_connection.cursor()
#     db_cursor.execute("""SELECT id_number , role, 
#                         swipes_remaining, dining_dollars
#                         FROM account_profile, meal_balance
#                         WHERE meal_balance.account_id = account_profile.account_id 
#                         AND account_profile.id_number = (%s)""", (stdid,))
#     info_result = db_cursor.fetchall()
#     for entry in info_result:
#         caf_db[entry[0]] = {
#             "student_id" : entry[0],
#             "swipes" : entry[2],
#             "dining_dolars" : entry[3],
#             "role" : entry[1]
#         }

#     return caf_db

# print(get_user_caf_db('529194'))
# print(get_user_caf_db())

# def get_account_id_db(stdid):
#     # account_id = []
#     db_connection = psycopg2.connect(**db_info)
#     db_cursor = db_connection.cursor()
    
#     db_cursor.execute("""SELECT account_id 
#                         FROM account_profile
#                         WHERE account_profile.id_number = (%s)""", (stdid,))
    
#     account_id_res = db_cursor.fetchall()
    
#     db_cursor.close()
#     return account_id_res[0][0]

# print(get_account_id_db("529194"))

def update_user_swipe_db(stdid, swipes):
    caf_db = {}
    db_connection = psycopg2.connect(**db_info)

    db_cursor = db_connection.cursor()
        
        
        
    # db_cursor.execute("""UPDATE meal_balance 
    #                         SET swipes_remaining = (%s)
    #                         WHERE meal_balance.account_id = (%s)""", (swipes, stdid,))
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="something wrong with db_connection",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
    db_cursor.execute ("""SELECT * FROM meal_balance 
                       WHERE meal_balance.account_id = (%s)""", (stdid,))
    return db_cursor.fetchall()
        
print(update_user_swipe_db(3, 99))