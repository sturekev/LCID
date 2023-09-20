from fastapi import FastAPI

#jsonFormat where keep all Put methods for imput Json from API
from Assets.jsonFormat import signinInput, HallTokenRequest, HallTokenVerify
#Authenticate for signin
from Authenticate.signin import signinAuth

app = FastAPI()

#get jsonData = inputJson.username
# right now only 1 step verification
@app.put("/signin")
def signInAPi(inputJson: signinInput):
    return signinAuth(inputJson.username, inputJson.password, inputJson.timestamp)


# APis give User a hash token to use for access
@app.put ("/HallAccess/{request}")
def requestHallAccess (request,iputJson: HallTokenRequest):
    if request == "request":
        pass
    pass

#Apis verify signal or verify qrcode
@app.put ("/HallAccess/{request}")
def verifyHallAccess (request, inputJson: HallTokenVerify):
    if request == "verify":
        pass
    pass

#Apis getDinningService user Data
@app.put ("/DinningService/request/{request}")
def requestDinningService():
    pass

@app.put ("/DinningService/verify/{reques}")
def verifyDinningService():
    pass