from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from decouple import config


ALGORITHM = config("algorithm")
CAF_SECRET_KEY = config("dinning_caf_secret")

def fake_users_Hall_db ():
    fake_HallAccess_db = {
        "johndoe": {
            "swipe": 20,
            "dinning_dolar":200,
            "role": "student"
        }
    }
    return fake_HallAccess_db

def get_access_hall_db(db,user:str):
    if user in db:
        user_dict = db[user]
        return user_dict
    
def create_caf_swipe_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, CAF_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_caf_swipe (token:str, location: str, role: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CAF_SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        swipes: str = payload.get("swipe")
        cafSwipe_db = get_access_hall_db(fake_users_Hall_db(),name)
        if not cafSwipe_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="something wrong with login token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if name is None or swipes is None:
            raise credentials_exception
        else: 
            if cafSwipe_db - swipes:
                return True, cafSwipe_db - swipes, None
            else: 
                return False, None, "Balance not enough"         

    except JWTError:
        raise credentials_exception
