# this is to access main.py
import sys

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')

from fastapi.testclient import TestClient

from main import app, get_current_active_user

sys.path.insert(1, '../Backend/Authenticate')
from signin import get_current_user

# sys.path.insert(1, '../Backend/Assets')
# from jsonFormat import User, UserInDB

sys.path.insert(1, '../Backend')
from Assets.jsonFormat import UserInDB, User, TokenData

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

client = TestClient(app)



async def overrride_get_current_active_user_right(
    # current_user: Annotated[User, Depends(get_current_user)]
):
    
    current_user = mock_user_right()
    
    # if current_user.disabled:
    #     print("current_active", current_user)
    #     print(type(current_user))
    #     raise HTTPException(status_code=400, detail="Inactive user")
    # return current_user

    get_current_active_user(current_user)





def mock_user_right():
    mock_user = {
        # "username": "johndoe",
        # "full_name": "John Doe",
        # "email": "johndoe@example.com",
        # "disabled": False,
        # "student_id": 529194
        
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "student_id" : 529194
    }
    
    user_data = UserInDB(**mock_user)
    # return user_data
    return mock_user
        

def test_user_me_right():
    app.dependency_overrides[get_current_active_user] = overrride_get_current_active_user_right
    response = client.get("/users/me")
    assert response.status_code == 200
    message = response.json()
    assert "username" in message
    assert "email" in message
    assert "full_name" in message
    assert "disabled" in message
    assert "student_id" in message
    