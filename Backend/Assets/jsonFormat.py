from pydantic import BaseModel

class signinInput(BaseModel):
    username: str
    password: str

class HallTokenRequest (BaseModel):
    userToken: str