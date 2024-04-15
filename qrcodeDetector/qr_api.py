from fastapi import FastAPI
#put fastapi method
app = FastAPI()
@app.get("/echo/{message}") #get chỉ nhận message?
def echo_message(message: str):
    return {"message": message}

# # tạo fake data 1 dictionary 
# def get_fake_user_resident():
#     fake_user_resident = {
#         "name" : "JohnDoe",
#         "resident": "miller"    
#     }
#     return fake_user_resident


# token = (secret_key + expire_token_time + data[user_name + resident + timestamp])
# token sẽ dc encrypt/decrypt=hs256  (thuật toán hash256)



# dùng tạo ecrypted fake token cho hall access
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# SECRET_KEY = secret trong .env (Tạm thời)
# data = fake_user_resident
# expires_delta:     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# algorithm: hs256 



# để decode token; sau khi decode ra payload là data[user_name + resident + timestamp]
#async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#    credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     username: str = payload.get("sub")
    #     if username is None:
    #         raise credentials_exception
    #     token_data = TokenData(username=username)
    # except JWTError:
    #     raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user



# check payload data với dictionary user_database:
# nếu user_name + resident != local_hall:
# check timestamp<=23h: grant access; else: not



# send_data.py gửi encrypted token + location (local_hall) (not encrypted) đến api
# api sẽ decrypt để lấy:
# token
# user_name
# timestamp

from pydantic import BaseModel

class MessageInput(BaseModel):
    message: str

@app.post("/receive_message/")
def receive_message(message_input: MessageInput):
    if message_input.message=="Hello, FastAPI!":
        return {"message": message_input.message}
    else:
        return {"Access Denied"}



#access là utilities của main features 
#authenticate là feature của product (Chức năng là authenticate)



# lấy timestamp vào caf để xác định breakfast, dinner, brunch
# 