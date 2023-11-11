from pydantic import BaseModel

#Input request Json 

# Hall acess verify
class HallTokenVerify (BaseModel):
    token: str
    location: str
    timestamp: str
class HallTokenData(BaseModel):
    name: str
    resident: str
# For Login 
class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

#
# APis Response Configuration 
#

# response for Login APis  
class AppToken(BaseModel):
    access_token: str
    token_type: str

#response for GetHallAcess
class HallAccessResponse(BaseModel):
    message : str
    token_type: str

# reponse for Hall Acess verify 
class HallAcessVerifyResponse(BaseModel):
    message :bool 