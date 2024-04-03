from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from decouple import config

import psycopg2
from psycopg2 import OperationalError

from Assets.database.db_config import get_db_info
filename='Assets/database/db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)


ALGORITHM = config("algorithm")
CAF_SECRET_KEY = config("dining_caf_secret")


def get_user_caf_db (student_id):
    caf_db = {}
    db_connection = psycopg2.connect(**db_info)

    db_cursor = db_connection.cursor()
    db_cursor.execute("""SELECT id_number, role, swipes_remaining, dining_dollars
                        FROM account_profile, meal_balance
                        WHERE meal_balance.account_id = account_profile.account_id 
                        AND account_profile.id_number = (%s)""", (student_id,))
    info_result = db_cursor.fetchall()
    for entry in info_result:
        caf_db[entry[0]] = {
            "student_id" : entry[0],
            "swipes" : entry[2],
            "dining_dolars" : entry[3],
            "role" : entry[1]
        }

    return caf_db

def get_account_id_db(student_id):
    db_connection = psycopg2.connect(**db_info)
    db_cursor = db_connection.cursor()
    
    db_cursor.execute("""SELECT account_id 
                        FROM account_profile
                        WHERE account_profile.id_number = (%s)""", (student_id,))
    
    account_id_res = db_cursor.fetchall()
    
    db_cursor.close()
    return account_id_res[0][0]

def update_user_swipe_db(student_id, swipes):
    db_connection = psycopg2.connect(**db_info)

    db_cursor = db_connection.cursor()
        
    db_cursor.execute("""UPDATE meal_balance 
                            SET swipes_remaining = (%s)
                            WHERE meal_balance.account_id = (%s)""", (swipes, student_id,))
    db_connection.commit()
    db_cursor.execute ("""SELECT * FROM meal_balance 
                       WHERE meal_balance.account_id = (%s)""", (student_id,))
    
    return db_cursor.fetchall()[0][2]

def get_user_dining_db(db,student_id: str):
    if student_id in db:
        user_dict = db[student_id]
        return user_dict
    
def create_caf_swipe_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    user_dining_db = get_user_dining_db(get_user_caf_db(str(data["student_id"])),str(data["student_id"]))

    if not user_dining_db :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= f"something wrong with create caf token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif int(user_dining_db["swipes"]) == 0 or int((user_dining_db["swipes"]) - int(data["swipes"])) < 0:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail= f"Balance not enough",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"student_id": user_dining_db["student_id"]})
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, CAF_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_caf_swipe (token:str, location: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, CAF_SECRET_KEY, algorithms=[ALGORITHM])
        student_id: str = payload.get("student_id")
        swipes: str = payload.get("swipes")
        caf_swipe_db = get_user_dining_db(get_user_caf_db(student_id), student_id)
        
        if not caf_swipe_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="something wrong with login token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if student_id is None or swipes is None:
            raise credentials_exception
        else: 
            if caf_swipe_db["swipes"] - int(swipes) >= 0 :
                res = update_user_swipe_db(get_account_id_db(student_id), caf_swipe_db["swipes"] - int(swipes))
                return True, caf_swipe_db["swipes"] - int(swipes), f"Success {res}"
            else: 
                return False, caf_swipe_db["swipes"], f"Balance not enough"          

    except JWTError:
        raise credentials_exception
