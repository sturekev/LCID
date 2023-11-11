from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

app = FastAPI()

# Secret key for JWT
SECRET_KEY = "60528e0f7a9ae5946dda2dd2d01f3904ccf2c7e22779b300095855b429b61303"

# Create a dependency for JWT token validation and extraction
def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token/"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # You can perform further validation or extract user information from the payload here
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid")

# Protect a route using the dependency
@app.get("/protected-route")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
