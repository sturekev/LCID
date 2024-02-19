from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from decouple import config


ALGORITHM = config("algorithm")
CAF_SECRET_KEY = config("dinning_caf_secret")

def fake_users_dinning_db ():
    fake_HallAccess_db = {
        "johndoe": {
            "student_id": 52194,
            "swipe": 20,
            "dinning_dolar":200,
            "role": "student"
        }
    }
    return fake_HallAccess_db

def fake_users_dinnining_db_verify():
    fake_HallAccess_db = {
        "52194": {
            "student_id": 52194,
            "swipe": 20,
            "dinning_dolar":200,
            "role": "student"
        }
    }
    return fake_HallAccess_db
def update_swipe (numSwipe):
    pass

def get_user_dinning_db(db,user:str):
    if user in db:
        user_dict = db[user]
        return user_dict
    
def create_caf_swipe_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    user_dinning_db = get_user_dinning_db(fake_users_dinning_db(),data["name"])
    if not user_dinning_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="something wrong with login token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"student_id": user_dinning_db["student_id"]})
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
        cafSwipe_db = get_user_dinning_db(fake_users_dinnining_db_verify(),str(student_id))
        if not cafSwipe_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="something wrong with login token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if student_id is None or swipes is None:
            raise credentials_exception
        else: 
            if cafSwipe_db["swipe"] - int(swipes) >= 0 :
                update_swipe(cafSwipe_db["swipe"] - int(swipes))
                return True, cafSwipe_db["swipe"] - int(swipes), "Success"
            else: 
                return False, cafSwipe_db["swipe"], f"Balance not enough {swipes}"         

    except JWTError:
        raise credentials_exception
