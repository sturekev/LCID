from pydantic import BaseModel

# {
#     'username': 'data',
#     'passowrd': 'data',
#     ..
# }
class signinInput(BaseModel):
    username: str
    password: str
    # timestamp: str

class HallTokenRequest (BaseModel):
    userToken: str
    timestamp: str

class HallTokenVerify (BaseModel):
    userToken: str
    HashAccessToken: str
    timestamp: str

class UserInfoVerify (BaseModel):
    userToken: str
    timestamp: str

