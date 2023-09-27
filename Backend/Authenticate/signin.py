

# verify signin username and password from db 
# return json return for APis (with redirect for 2 step Auth , or a error)
def signinAuth (username:str, password: str) -> dict:
    verify, data = verifyUsername(username)
    msg = ""
    userToken = ""
    if verify:
        verify, data = verifyPassword (password,data["dbPassword"], data["salt"])
        if verify:
            return data
        return False

def generateSigninJson(msg,data=""):
    return

# connect to db and verified it
# return bool and userToken as str
def verifyPassword (password: str, dbPassword: str, salt:str):
    pass

#from Account table
# select username, password, salt from Account where username = username
# return password 
def verifyUsername (username: str):
    return 