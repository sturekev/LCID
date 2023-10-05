from Backend.Assets.Utils import getCurrentDatetime
from Backend.Assets.database.signInDB import getAccountPass
from Backend.Authenticate.hash import *
# verify signin username and password from db 
# return json return for APis (with redirect for 2 step Auth , or a error)
def signinAuth (username:str, password: str):
    verify, data = verifyUsername(username)
    if verify:
        if not checkPassword(endcodePassword=encodePassword(password), hashed=data["Password"]):
            verify = False
            data = ["Password wrong, please try again!"]

    return generateSigninJson(verify,data)


def generateSigninJson(verified,data):
    Response = {
                    "Success": False,
                    "Response": {"MSG":""},
                    "Timestamp": ""
                    }

    Response["Success"] = verified
    Response["Response"]["MSG"] = data[0]
    Response["Timestamp"] = getCurrentDatetime()

    if verified:
        Response["Response"]["User Token"] = data[3]
        return Response
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