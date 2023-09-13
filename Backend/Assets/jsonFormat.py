from pydantic import BaseModel

class signinInput(BaseModel):
    username: str
    password: str