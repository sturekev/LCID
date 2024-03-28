# this is to access main.py
import sys

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')

from fastapi.testclient import TestClient

from main import app, get_current_active_user

sys.path.insert(1, '../Backend/Authenticate')
from signin import get_current_user, get_current_active_user

# sys.path.insert(1, '../Backend/Assets')
# from jsonFormat import User, UserInDB

sys.path.insert(1, '../Backend')
from Assets.jsonFormat import UserInDB, User, TokenData

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

client = TestClient(app)


def override_dependency_get_current_active():
    mock_user = {
        "username": "tuph01",
        "full_name": "Kevin Tu",
        "email": "tuph01@luther.edu",
        "disabled": False,
        "student_id": 529194,
        "hashed_password": "$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm"
    }
    user_data = UserInDB(**mock_user)
    
    # data2 = get_current_active_user(user_data)
    # return data2
    return user_data



async def override_dependency_right():
    mock_user = {
        # "username": "johndoe",
        # "full_name": "John Doe",
        # "email": "johndoe@example.com",
        # "disabled": False,
        # "student_id": 529194
        # "username": "johndoe",
        # "full_name": "John Doe",
        # "email": "johndoe@example.com",
        # "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        # "disabled": False,
        # "student_id" : 529194
        
        "username": "tuph01",
        "full_name": "Kevin Tu",
        "email": "tuph01@luther.edu",
        "disabled": False,
        "student_id": 529194,
        "hashed_password": "$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm"
    }
    
    user_data = UserInDB(**mock_user)
    return user_data
        
            
async def override_dependency_disabled():
    mock_user = {
       "username": "tuph01",
        "full_name": "Kevin Tu",
        "email": "tuph01@luther.edu",
        "disabled": True,
        "student_id": 529194,
        "hashed_password": "$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm"
    }
    
    user_data = UserInDB(**mock_user)
    return user_data

def test_user_me_disabled():
    app.dependency_overrides[get_current_user] = override_dependency_disabled
    response = client.get("/users/me")
    assert response.status_code == 401
    message = response.json()

    assert message["detail"]=="Not authenticated"
    
    
# def convoi():
#     mock_user = {
#         "username": "jevin",
#         "full_name": "jev Doe",
#         "email": "jev@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": True,
#         "student_id" : 529194
#     }
    
#     user_data = UserInDB(**mock_user)
#     print(user_data)
#     print(type(user_data))
#     print(user_data.disabled)
#     return user_data
    
#     # user_data = Annotated[User, mock_user]
#     # print(user_data[1])
#     # print(type(user_data[1]))
#     # return user_data
# convoi()


def test_user_me_right_new():
    app.dependency_overrides[get_current_active_user] = override_dependency_get_current_active
    response = client.get("/users/me")
    assert response.status_code == 200
    message = response.json()
    assert "username" in message
    assert "email" in message
    assert "full_name" in message
    assert "disabled" in message
    assert "student_id" in message
    




def test_user_me_right():
    app.dependency_overrides[get_current_user] = override_dependency_right
    response = client.get("/users/me")
    assert response.status_code == 200
    message = response.json()
    assert "username" in message
    assert "email" in message
    assert "full_name" in message
    assert "disabled" in message
    assert "student_id" in message
    
print(override_dependency_get_current_active())
    