#this file contain all of the function suport Hall Access request/verify APis 
# Feature update UserToken 
# Feature update UserPublicKey for User Access
# Feature update UserPrikey for user
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

def users_hall_db():
    hall_access_db = {}
    db_connection = psycopg2.connect(**db_info)

    db_cursor = db_connection.cursor()
    db_cursor.execute('''SELECT username, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    info_result = db_cursor.fetchall()
    for entry in info_result:
        hall_access_db[entry[0]] = {
            "resident": entry[1]
        }
    
    return hall_access_db

def get_access_hall_db(db,user:str):
    if user in db:
        user_dict = db[user]
        return user_dict
    
def create_access_Hall_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    hall_db = get_access_hall_db(users_hall_db(), data["name"])
    if not hall_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="something wrong with create Hall access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"resident": hall_db["resident"]})
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, HALL_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def verify_Hall_access (token:str, location: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    building = ['Farwell', 'Olson', 'Diseth', 'Miller', 'Brandt', 'Ylvisaker', 'Baker Village', 'College Apartments', 'Larsen', 'Prairie Houses', 'Sustainability House', 'Off-Campus Living', 'Roth']
    try:
        payload = jwt.decode(token, HALL_SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        resident: str = payload.get("resident")
        print(resident + " Hello")
        if name is None or resident is None:
            raise credentials_exception
        else: 
            if resident == "Super":
                return True
            if location not in building:
                raise credentials_exception
            elif resident == location:
                return True
            else: 
                current_time = datetime.now().time()  # Get the current time

                # Check if the current time is earlier than 11 PM (23:00)
                if current_time < datetime.strptime('23:00:00', '%H:%M:%S').time() and current_time > datetime.strptime('08:00:00', '%H:%M:%S').time():
                    return True  
                else: return False          

    except JWTError:
        raise credentials_exception


