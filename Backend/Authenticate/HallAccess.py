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

# from Assets.jsonFormat import

ALGORITHM = config("algorithm")
HALL_SECRET_KEY = config("hall_secret")

def fake_users_Hall_db ():
    fake_HallAccess_db = {
        "johndoe": {
            "resident": "miller",
        }
    }
    return fake_HallAccess_db

def get_access_hall_db(db,user:str):
    if user in db:
        user_dict = db[user]
        return user_dict
def create_access_Hall_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    hall_db = get_access_hall_db(fake_users_Hall_db(),data["name"])
    if not hall_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="something wrong with login token",
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
    try:
        payload = jwt.decode(token, HALL_SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        resident: str = payload.get("resident")
        
        if name is None or resident is None:
            raise credentials_exception
        else: 
            if resident == "Super":
                return True
            if resident == location:
                return True
            else: 
                current_time = datetime.now().time()  # Get the current time

                # Check if the current time is earlier than 11 PM (23:00)
                if current_time < datetime.strptime('23:00:00', '%H:%M:%S').time() and current_time > datetime.strptime('08:00:00', '%H:%M:%S').time():
                    return True  
                else: return False          

    except JWTError:
        raise credentials_exception


