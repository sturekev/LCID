from fastapi import FastAPI

#jsonFormat where keep all Put methods for imput Json from API
from Assets.jsonFormat import signinInput,
#Authenticate for signin
from Authenticate.signin import signin

app = FastAPI()

#get jsonData = inputJson.username
# right now only 1 step verification
@app.put("/signin")
def signInAPi(inputJson: signinInput):
    return signinAuth(inputJson.username, inputJson.password)



@app.put ("/HallAccess")
def sendHallAccessToken (inputJson:)