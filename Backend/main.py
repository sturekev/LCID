
#Fastapi packages
from datetime import timedelta, datetime
from typing import Annotated
from fastapi import FastAPI, HTTPException, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn

from decouple import config

#jsonFormat where keep all Put methods for imput Json from API
from Assets.jsonFormat import HallAccessResponse, HallAcessVerifyResponse
from Assets.jsonFormat import AppToken, User
#Authenticate for signin
from Authenticate.signin import authenticate_user, create_access_token, fake_users_db, get_current_active_user
#Auth for Hall
from Authenticate.HallAccess import create_access_Hall_token, verify_Hall_access
#Auth for Caf
from Authenticate.verifycaf import verify_caf

# from user_profile.user_profile import get_user_profile

ACCESS_TOKEN_EXPIRE_MINUTES  = 30
HALL_ACCESS_TOKEN_EXPIRE_MINUTES  = 5

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login/", response_model=AppToken)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}

# APis give User a hash token to use for access
@app.get("/HallAccess/me/", response_model=HallAccessResponse)
async def GetHallAcess(
    current_user: Annotated[User, Depends(get_current_active_user)]
   
):
    
    access_token_expires = timedelta(minutes=HALL_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_Hall_token(
        data={"name": current_user.username}, expires_delta=access_token_expires
        )
    
    return {"message":access_token, "token_type": "Bearer"}

@app.post("/HallAccess/{location}/{token}/", response_model=HallAcessVerifyResponse)
async def verifyHallAccess(location, token):
    response = verify_Hall_access(token, location)
    return {"message": response}
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@app.get("/echo/{token}")
async def caf_entry(token:str):
    response = verify_caf(token)
    return response


# @app.get("/user_profile/")
# async def get_user_profile(user_profile: Annotated[User, Depends(get_user_profile)]):
#     return user_profile


# #Apis getDinningService user Data
# @app.put ("/DinningService/request/{request}")
# def requestDinningService():
#     pass

# @app.put ("/DinningService/verify/{request}")
# def verifyDinningService():
#     pass

# @app.put ("test/{link}")
# def test(link, inputJson: signinInput):
#     return {"link": link, "jsonInput": inputJson}
