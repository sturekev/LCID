from fastapi import FastAPI, HTTPException
import asyncio
#jsonFormat where keep all Put methods for imput Json from API
from Assets.jsonFormat import signinInput, HallTokenRequest, HallTokenVerify
from Assets.jsonFormat import loginResponse
#Authenticate for signin
from fastapi.responses import JSONResponse
from Authenticate.signin import signinAuth
from Authenticate.token import verifyUserToken
from Authenticate.HallAccess import getHallToken, updatHallToken

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#get jsonData = inputJson.username
# right now only 1 step verification
@app.post("/signin/",response_model=loginResponse)
async def sign_in(input_json: signinInput) -> loginResponse:
    username = input_json.username
    password = input_json.password

    success, user_data = signinAuth(username, password)

    if success:
        return loginResponse(message=user_data)
    else:
        raise HTTPException(status_code=401, detail=user_data)


# APis give User a hash token to use for access
@app.post ("/HallAccess/getToken/{request}")
async def requestHallAccess (request,iputJson: HallTokenRequest):
    verifyToken, response = verifyUserToken()
    if verifyToken:
        if request == "getToken":
            return getHallToken()
        elif request == "resetToken":
            return updatHallToken()
    else:
        raise HTTPException(status_code=401, detail=response)


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