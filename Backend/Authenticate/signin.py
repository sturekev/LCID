from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from decouple import config

from Assets.database.signInDB import getAccountPass
from Authenticate.hash import *
from Assets.jsonFormat import TokenData, User, UserInDB

import psycopg2
from psycopg2 import OperationalError

from Assets.database.db_config import get_db_info

filename='Assets/database/db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)

def users_db ():
    users_db = {}
    db_connection = psycopg2.connect(**db_info)

    db_cursor = db_connection.cursor()
    db_cursor.execute('''SELECT fullname, username, password, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    info_result = db_cursor.fetchall()
    for entry in info_result:
        users_db[entry[1]] = {
            "username": entry[1],
            "full_name": f"{entry[0]}",
            "email": f"{entry[1]}@luther.edu",
            "hashed_password": entry[2],
            "disabled": False,
            "student_id": entry[3],
            "building": entry[4]
        }

    return users_db


SECRET_KEY = config("secret")
ALGORITHM = config("algorithm")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        print("get_user", UserInDB(**user_dict))
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):

        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(payload)
        print(payload.get("sub"))
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(users_db(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Disabled user")
    return current_user

