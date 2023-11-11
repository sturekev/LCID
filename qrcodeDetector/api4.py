from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

app = FastAPI()

# Your secret key to verify the token. Keep it secret!
SECRET_KEY = "60528e0f7a9ae5946dda2dd2d01f3904ccf2c7e22779b300095855b429b61303"

# Dependency to get the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Verify and decode the JWT token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid")

@app.get("/echo/{token_data}")
def echo_data(token_data: dict = Depends(verify_token)):
    return token_data
