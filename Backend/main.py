
#Fastapi packages
from datetime import timedelta, datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn

from decouple import config

#jsonFormat where keep all Put methods for imput Json from API
from Assets.jsonFormat import HallAccessResponse, HallAcessVerifyResponse
from Assets.jsonFormat import AppToken, User, userProfile
from Assets.jsonFormat import dinningCaf, diningCaf_response
from Assets.jsonFormat import library_iD

#Authenticate for signin
from Authenticate.signin import authenticate_user, create_access_token, users_db, get_current_active_user
#Auth for Hall
from Authenticate.HallAccess import create_access_Hall_token, verify_Hall_access
from profileDashboard.dashBoard import get_user_profile
from DinningService.caf import create_caf_swipe_token, verify_caf_swipe

ACCESS_TOKEN_EXPIRE_MINUTES  = 30
FEATURE_ACCESS_TOKEN_EXPIRE_MINUTES  = 5

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login/", response_model=AppToken)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(users_db(), form_data.username, form_data.password)
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
    
    access_token_expires = timedelta(minutes=FEATURE_ACCESS_TOKEN_EXPIRE_MINUTES)
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


@app.get("/dinningservice/caf/me/{swipes}/", response_model=dinningCaf)
async def getSwipe(
    swipes, current_user: Annotated[User, Depends(get_current_active_user)]
):
    
    access_token_expires = timedelta(minutes=FEATURE_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_caf_swipe_token(
        data={"student_id": current_user.student_id, "swipes": swipes}, expires_delta=access_token_expires
        )
    
    return {"message":access_token, "token_type": "Bearer"}


@app.post("/dinningservice/caf/{token}/{location}/", response_model=diningCaf_response)
async def verifyCafAccess(token, location):
    success, swipe, response = verify_caf_swipe(token, location)

    if success:
        return { "swipes": swipe, "message": response}
    return { "swipes": swipe, "message": response}

@app.post("/library/me/", response_model = library_iD)
async def library_student_id (
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return {"message": current_user.student_id} 

@app.get("/user/profile", response_model = userProfile)
async def getUserProfile(
    current_user: Annotated[User, Depends(get_current_active_user)]
): 

    return get_user_profile( str(current_user.student_id))
