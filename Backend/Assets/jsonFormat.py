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
    username: str

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    student_id : int | None = None

class userProfile(BaseModel):
    full_name : str
    student_id : int
    residence : str
    swipes : int
    dinning_dolar: int

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
    
class dinningCaf(BaseModel):
    message : str
    token_type: str
    
class diningCaf_response (BaseModel):
    swipes: int
    message: str
    
    

# Caf feature
class CafVerifyResponse(BaseModel):
    success : bool
    swipes: int | None = None
    message : str | None = None

    
class library_iD (BaseModel):
    message : int