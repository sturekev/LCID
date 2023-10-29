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

class loginResponse(BaseModel):
    message: dict
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



# class User (BaseModel):
#     email : str
    
class AppToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
    
class UserHalTokenInDB(User):
    resident: str
    