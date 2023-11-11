# from datetime import timedelta, datetime
# from typing import Annotated
from fastapi import FastAPI, HTTPException, Body, Depends, status
# from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from pydantic import BaseModel
from jose import JWTError, jwt

SECRET_KEY='abcd'

class caf_response(BaseModel):
    message : str

def verify_swipes (token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = str(jwt.decode(token, SECRET_KEY, algorithms=["HS256"]))
        return payload 

    except JWTError:
        raise credentials_exception

app = FastAPI()

@app.get("/echo/{token}",response_model=caf_response)
async def caf_entry(token):
    response =  verify_swipes(token)
    return {"message": response }
    # return type(token)