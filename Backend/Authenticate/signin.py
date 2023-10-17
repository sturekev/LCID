from fastapi import FastAPI, HTTPException

from Backend.Assets.Utils import getCurrentDatetime
from Backend.Assets.database.signInDB import getAccountPass
from Backend.Authenticate.hash import *
# verify signin username and password from db 
# return json return for APis (with redirect for 2 step Auth , or a error)
def signinAuth (username:str, password: str):
    # verify, data = verifyUsername(username)
    verify, data = mockDataForFunction(username=username)
    if verify:
        if not checkPassword(endcodePassword=encodePassword(password), hashed=data["Password"]):
            verify = False
            data = ["Password wrong, please try again!"]

    return verify, generateSigninJson(verified=verify, data=data)


def generateSigninJson(verified,data):
    Response = {
                    "Success": False,
                    "Response": {"MSG":""},
                    "Timestamp": ""
                    }

    Response["Success"] = verified
    
    Response["Timestamp"] = getCurrentDatetime()

    if verified:
        Response["Response"]["User Token"] = data["username"]
        return Response
    Response["Response"]["MSG"] = data
    return Response

#from Account table
# select username, password, salt from Account where username = username
# return password 
def verifyUsername (username:str):
    # Todo: Execute data from db and save executed data
    data = getAccountPass(username)
    if data: 
        return True, data 
    return False, ["Username wrong, please try again!"]

def mockDataForFunction(username: str):
    data = {
        "testing00" : {
            "username": "testing00",
            "Password": hashedPassword(endcodePassword=encodePassword("testing00"))
        },
        "testing01" : {
            "username": "testing01",
            "Password": hashedPassword(endcodePassword=encodePassword("testing01"))
        },
        "testing02" : {
            "username": "testing02",
            "Password": hashedPassword(endcodePassword=encodePassword("testing02"))
        },
    }
    if username in data:
        return True, data[username]
    return False, ["Username wrong, please try again!"]

