# from typing import Annotated
# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer

# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from decouple import config

# from Assets.database.signInDB import getAccountPass
# from Authenticate.hash import *
# from Assets.jsonFormat import TokenData, User, UserInDB
# # verify signin username and password from db 
# # return json return for APis (with redirect for 2 step Auth , or a error)

# def fake_users_db ():
#     fake_users_db = {
#         "johndoe": {
#             "username": "johndoe",
#             "full_name": "John Doe",
#             "student_id": "01234567",
#             "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#             "disabled": False,
#         },
#         "jevin": {
#             "username": "jevin",
#             "full_name": "jev Doe",
#             "student_id": "09876543",
#             "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#             "disabled": True,
#         }
#     }
#     return fake_users_db



# SECRET_KEY = config("secret")
# ALGORITHM = config("algorithm")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# async def get_user_profile(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db(), username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_user_profile)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
