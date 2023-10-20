from Assets.Utils import getCurrentDatetime
from Authenticate.hash import *
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
        Response["Response"]["User Token"] = data[1]
        return Response
    return Response

#from Account table
# select username, password, salt from Account where username = username
# return password 
def verifyUsername (username:str, db):
    # Todo: Execute data from db and save executed data
    #
    # if username == data.username:
    #     return True, data
    return False, ["Username wrong, please try again!"]
  
# verify signin username and password from db 
# return json return for APis (with redirect for 2 step Auth , or a error)
def signinAuth (username:str, password: str) -> dict:
    pass 


# connect to db and verified it
# return bool and userToken as str
def signDb (username: str, password: str):
    pass
