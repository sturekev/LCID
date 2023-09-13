from fastapi import FastAPI

#jsonFormat where keep all Put methods for imput Json from API
from Assets.jsonFormat import signinInput
#Authenticate for signin
from Authenticate.signin import signin

app = FastAPI()

#get jsonData = inputJson.username
@app.put("/signin")
def signInAPi(inputJson: signinInput):
    verify,data =  signinAuth(inputJson.username, inputJson.password):
    if verify:
        return {
                    "message": "Login Successfully!",
                    "data": data
                    }
    return {"message": "Item created successfully!"}
