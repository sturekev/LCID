from jose import JWTError, jwt
from fastapi import FastAPI,Depends, HTTPException, status
from datetime import datetime, timedelta
SECRET_KEY="60528e0f7a9ae5946ddasdd2d012f3904ccf2c7vbe227zxcv79b300095855b429b61303"

def verify_caf(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # print(payload)
        # print(type(payload))
        caf_swipes_left: int = payload.get("caf_swipes_left")

        current_time = datetime.utcnow()
        # don't have to check if exp<current_time because jwt will auto check exp
        if caf_swipes_left>0:
            payload["caf_swipes_left"]-=1
            # print("update user_swipes",payload)
            return_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return_payload = {
                "message": "Entry Granted. Bon Appétit",
                "return_token": return_token,
                "enter_time" : str(current_time)
            }

            # print(return_payload)
            return return_payload 
        else:
            return_payload={"message":"Entry Denied. Zero swipes left"}
            return return_payload
    except JWTError:
        raise credentials_exception