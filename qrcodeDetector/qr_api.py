from fastapi import FastAPI
#put fastapi method
app = FastAPI()
@app.get("/echo/{message}") #get chỉ nhận message?
def echo_message(message: str):
    return {"message": message}

from pydantic import BaseModel

class MessageInput(BaseModel):
    message: str

@app.post("/receive_message/")
def receive_message(message_input: MessageInput):
    if message_input.message=="Hello, FastAPI!":
        return {"message": message_input.message}
    else:
        return {"Access Denied"}

