from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from decouple import config
import psycopg2

ALGORITHM = config("algorithm")
HALL_SECRET_KEY = config("hall_secret")

from Assets.database.db_config import get_db_info

filename='Assets/database/db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)

def user_profile_db (stdid):
    hall_access_db = {}
    db_connection = psycopg2.connect(**db_info)

    db_cursor = db_connection.cursor()
    db_cursor.execute('''SELECT * 
                        FROM account, account_profile, building_info, meal_balance
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing
                        AND account_profile.account_id  = meal_balance.account_id
                        AND account_profile.id_number = (%s)''', (stdid,))
    info_result = db_cursor.fetchall()
    for entry in info_result:
        hall_access_db[entry[4]] = {
            "full_name": entry[1],
            "student_id": entry[4],
            "residence": entry[9],
            "role": entry[11],
            "swipes": entry[12],
            "dining_dolars": entry[13]
        }
    return hall_access_db

def get_user_profile_db (db, stdid):
    if stdid in db: 
        user_dict = db[stdid]
        return user_dict
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="something wrong with db_connection",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_profile (data: str):
    
    user_db = get_user_profile_db (user_profile_db(data), data)
        
    return user_db