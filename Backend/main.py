from fastapi import FastAPI
from fastapi import FastAPI, HTTPException

#jsonFormat where keep all Put methods for imput Json from API
from Backend.Assets.jsonFormat import signinInput, HallTokenRequest, HallTokenVerify
from Backend.Assets.jsonFormat import signinInput
#Authenticate for signin
from fastapi.responses import JSONResponse
from Backend.Authenticate.signin import signinAuth
from Backend.Authenticate.token import verifyUserToken
from Backend.Authenticate.HallAccess import getHallToken, updatHallToken

app = FastAPI()

#get jsonData = inputJson.username
# right now only 1 step verification
@app.post("/signin/")
async def sign_in(input_json: signinInput):
    username = input_json.username
    password = input_json.password

    success, user_data = signinAuth(username, password)

    if success:
        return user_data
    else:
        raise HTTPException(status_code=401, detail=user_data)


# APis give User a hash token to use for access
@app.put ("/HallAccess/getToken/{request}")
async def requestHallAccess (request,iputJson: HallTokenRequest):
    verifyToken, response = verifyUserToken()
    if verifyToken:
        if request == "getToken":
            return getHallToken()
        elif request == "resetToken":
            return updatHallToken()
    else:
        raise HTTPException(status_code=401, detail=response)

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)