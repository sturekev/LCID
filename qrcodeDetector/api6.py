from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import BaseModel


SECRET_KEY = "abcd"
app = FastAPI()
class check_caf_reponse(BaseModel):
    message: str
@app.get("/echo/{token}", response_model = check_caf_reponse)
async def check_caf(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = str(jwt.decode(token, SECRET_KEY, algorithm=["HS256"]))
        if payload:
            result = {"message": "True"}
        else: result =  {'message': "False"}
    except jwt.DecodeError:
        raise credentials_exception
    return result

        # raise HTTPException(status_code=401, detail="Token is invalid")
    

