#this file contain all of the function suport Hall Access request/verify APis 
# Feature update UserToken 
# Feature update UserPublicKey for User Access
# Feature update UserPrikey for user
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from decouple import config


from Assets.jsonFormat import TokenData, User, UserHalTokenInDB, UserInDB

from Authenticate.hash import *

SECRET_KEY = config("secret")
ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES  = config("expire_token_time")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# from Assets.Utils import getCurrentDatetime
def fake_usersToken_db ():
    fake_HallAccess_db = {
        "johndoe": {
            "username": "johndoe",
            "resident": "miller",
        }
    }
    return fake_HallAccess_db
def fake_building_info():
    fake_building_info_db = {
        "miller":{
            "name": "Miller",
            "resident": b'MIIEpAIBAAKCAQEAuE7axaBPzvf0QWsW7jQxk145Msh0RQwht5yhYcpBN6mckRwjfaUy2tjiy6t89S0i3w/ZmWEgEqf+PQVq97Ga/gjLQmii1O87mnyqz+UUsJjKv5aUaGL3LdLaEO2DqIibeNmS1qxBqja23hJ02RXsf7HJlWHEP7Ic7htufJHJSgubap1f5YqB07CN8NWeYNSU0qG0bU2mqXHph7v7yffd78Cw7fGxRG295gTuTdbffi6xkT3CZOw0DONMH+oTW8XKyEvJKx5gQAqn59bmNWvgtlxPDmMsGbNH52VMppRPZ3/nIIpfgRc86uPQJbBtg00dGLzGYjRHs7H4cx2f7ZIywwIDAQABAoIBAFLcvPX597ek+c9JjsMkex92zr96qO98H1KWHGZDUOPuISKKZJhyI7WJqhmIbYMrOlDQJvQS2yEYHzEfFPLsijLpED04nvCd6A2yO/eA1jb5UrolQG7YA6o58GmI51bnqAKCy0YxpsoYlEmuQZNyDGRysZ80F8/NS71vXtKplrZvUP1VYAGEwDoVPah8udYtFEC7hbOPqXnDuJypLxZSxeP2n/GOJ+uh4PFLDCIi2WYfHPHELRPf/8ooA9y9Sdyyek/ahv9dH3P4vzZY8BJK2mjg1Jq4++n/KAIq5wnL4JZL2U8Vo0BM1M0IIVJ5Tlf6L/fr2dzY9PCbuNSNmW1+j/kCgYEAuxC1vyMiD0T2NCoKdzhVJLhy4Ltk1kD1ZWTB0QYaxO5gNm1FGEzTDCaGim4hEhhhYvO4Aj5OUr/L7wZUtYqu9d8smtxc86lTI+TFfQB2faWpVQe4gO957SN2vLTSablIknkN8FMVYX6yRejrRRNfmV0ojsRVDL/53yGWfm2eVvsCgYEA/DoIUc3milkONHQUr0JCfCIOfB+mVHkJP3kaXB6eqkhM4fIG3tUoC60QztyLG2yeMYycAeDZGDcHWcqyFLDW0vG1FWGqNLnIFlU3Ol/QmTNmCnSUKzO4SbqY0Z0z0h8TL5lEl0TFLAWfedHYUCvXOHbIAafQKGAobX1QUw/l6NkCgYEAg69ssgQSevtJ8kjSG0Edtv7dZ9SjVKxf06PNSM7qU02Xj1j2tfeG7lvEhHiocSuWiukU1Qd1bY01C6vCQBZDujQEG3QbPzAopfDrEWcdArB29rO7r5BlnYlEke0c3m4fZ3UuWcqzF3HwH4Sq8nKD7tuErJQLZzFRvkDPx2p1d7cCgYEAxRRzO7gu0xsSxlmNcAPN/0B9IO95/7czSq1Ns30ZbORhboq2Y5caW0U3ROt+pkcQtJaxr6YI+6rDy51d2Fz0/o5ud+6AGAKyHQEozivfylUm/jRpMfiPnsx2bBLxUtWFIEQaHDhX+DXMjlsxMjOPT0dAsEp3k5TPAf5QrRZXBsECgYBzic6tXRVm1ws7D+5ROKOgqt2jqsf5NjWAY8ejCbs3CROtqhx0QzsmaXR3tvuZYzk+vArgpxZtsgnhBdKLRmtlAtxzioPbrLsPnWnUODClh0m6FEh49Q0hE33+fzLybbqLzNfhkHAPqvuaD13Mvf5c/i0Cmf3GUphRIcgJVF4wBw=='
        },
        "general":{
            "token":b'MIIEowIBAAKCAQEA4MODP/QUSR/VuR4YpE2pzQYtW46wrGhg794p20erhmsPv5kJzWxFx+BEi6sH+v+fWLCRls4pv9rCOyr0K+EIrAGsnM1hLcOxXzLJv6F/o4ll+7+wPMtubKUfYxRvHCuSIn0WG0LwfcTkWHjQDYK8F3CvvDSmTwEAsPTIQHxyMyj3O5Vt1LpI00OzubE7SSdINzROwst7Q5v/B07Xho9knOEPnynlN1ZFOrpLr21yKh7ngiIee2ya09BpAXu7I9VI+npD9lnl81KrCdx1YnfdIlXy5stYcyDm4wZSm/QRFKd6KPRr3xTqHaA5FGZ+X83ahYALu9FB+t7bW67XuIquDwIDAQABAoIBAALo+UUYHOApWUgnLxVOiqDvObAmmJO7wvkYEzLOy7UP00cdL3f4voe7JjPmEGVZsXjottnYLqxrYZ/1TZkxxAT6P67Xvu4iKiAJCr9cycfUVw/7lmkTGFCc+hjodBSQecc5knz1pgYh87rnvAzTGg32TiHziBzjOqh4KfqJ/APLA3gu2EJSX1eSAD8/2/g7lVaNmQSGvK2qX9rybHJ7xcYUrpSuq+M/I7RaL/s7TxCjXW1LVy7ZuheI8cQy1iZTxX6gO+lPe+hufB0AA1Am5ZHrVUEKHw7l9yzxnZudFDQbZ1T3pvkq4L7OevXgPoPfC5DwYGykAWnC5ZFE5Jw9LBECgYEA4YzmO5PMlBZJFD0A0vo2EJxzt21LzWKpVM+32PCPM+H2/U8XuGP3+MlYzDUeFyF/3XoUo77Kdco+ByD4fnGHbtgJPXhNS728Nn72dZTm4AqLJ5AMYDvSeWcINECGABSIYT8J1WRf9b3un+PE25Dw2uquJLDN4vc40bubB+lOULUCgYEA/xttBg3lRTcK5ykp57A5qnS++juJdj54irWpdUtyjvj449deriKpxb8YoZPpbL/hwGsXo1SvW9Wt4WMLyr+266t5T5jZNqxLlJbLWt4Kcj4SERCgaYy0C6jaVDQLz7LNlV8PUvDztm4YoJ0mIgZJIgalPdPW7Sza02FuIqYAcjMCgYAqTqidAkM8f9WjYzH1YROlGAOoo2q1ks0aaIAexDjITZlruFtFrhLEatgqLciAJDt8yrp2YIJPh+kMo0WZSihSRVmuWxN8opFcU4JdWdnYqoGhoSaBIpd/SDFEw9meyDswqodorJRHXyIUgb/aQ5y6I40YusVTznWs+ZjB6iRThQKBgQDGOJ5HJQbv+Cv9oAuSnmjAXQSD1T0jZrktNqicnmo+U5C5IQDNl9uI7sqJyi+HM7WLWOs+GzBC0E7Soa5o9PyCNHQHeEHXbJsxstYCHiPJzxcksWGjghPoN2SmJubClTGPDhUPInCMYRG7wz/9EhtDWByPZQpMshy6QKteOtR/5wKBgFT09WkiF2n/EW77F03qtkMLePKZN5jsM0nhPmvNt/1VcRIZYaeHEc99vt/KdpfSQJk1t4rqlYC2PRbgxnD0bRw+p++8IGmTG91iVnzel7Rv23xrIW1/9gbJEwJGa/64spOSR8zyY/akkNgC+dfCLM7n9Nqc0rnapfaRfFzJP/5O' 
        }
    }
    return fake_building_info_db
def access_token(db,user):
    if user in db:
        user_dict = db[user]
        return UserHalTokenInDB(**user_dict)
    

# async def get_current_Hall(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = access_token(fake_usersToken_db(), username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
# async def get_access_Token(current_user: Annotated[User, Depends(get_current_Hall)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
# def hashToken_hall (userToken, data,expires_delta: timedelta | None = None):
#     toEncode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     toEncode.update({"exp": expire})
#     token = EncryptPubKey(userToken["buildingToken"],toEncode)
#     return token


def updatHallToken ():
    pass

def getHallToken ():
    pass


