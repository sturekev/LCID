
#Fastapi packages
from datetime import timedelta, datetime
from typing import Annotated
from fastapi import FastAPI, HTTPException, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn

from decouple import config

#jsonFormat where keep all Put methods for imput Json from API
from Assets.jsonFormat import UserHalTokenInDB, signinInput, HallTokenRequest, HallTokenVerify
from Assets.jsonFormat import loginResponse, AppToken, TokenData, User
#Authenticate for signin
from fastapi.responses import JSONResponse
from Authenticate.signin import authenticate_user, create_access_token, fake_users_db, get_current_active_user
from Authenticate.token import verifyUserToken
from Authenticate.HallAccess import get_access_Token, getHallToken, updatHallToken

ACCESS_TOKEN_EXPIRE_MINUTES  = 30

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
@app.get("/HallAccess/me/", response_model=UserHalTokenInDB)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
   
):
    
    return current_user


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
#setUp user token
#class of token
#user login and signup


# #Apis verify signal or verify qrcode
# @app.put ("/HallAccess/{request}")
# def verifyHallAccess (request, inputJson: HallTokenVerify):
#     if request == "verify":
#         pass
#     pass

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


# @app.put ("/HallAccess")
# def sendHallAccessToken (inputJson):
#     pass
