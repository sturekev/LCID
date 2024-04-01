# this is to access main.py
import sys
import pytest


# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')

from fastapi.testclient import TestClient

from main import app, get_current_active_user

sys.path.insert(1, '../Backend/Authenticate')
from signin import get_current_user

from unittest.mock import patch, Mock, call


sys.path.insert(1, '../Backend/Assets')
from jsonFormat import User, UserInDB

sys.path.insert(1, '../Backend')
from Assets.jsonFormat import UserInDB, User, TokenData

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

client = TestClient(app)


async def override_dependency_right():
    mock_user_right = {
        "username": "tuph01",
        "full_name": "Kevin Tu",
        "email": "tuph01@luther.edu",
        "disabled": False,
        "student_id": 529194,
        "hashed_password": "$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm"
    }
    user_data = UserInDB(**mock_user_right)
    return user_data
    

async def override_dependency_disabled():
    mock_user_disabled = {
        "username": "tuph01",
        "full_name": "Kevin Tu",
        "email": "tuph01@luther.edu",
        "disabled": True,
        "student_id": 529194,
        "hashed_password": "$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm"
    }
    user_data = UserInDB(**mock_user_disabled)
    return user_data

 
def test_authorize_right():
    app.dependency_overrides[get_current_active_user] = override_dependency_right
    response_HA_me = client.get("/users/me")
    assert response_HA_me.status_code == 200
    



# def test_authorize_right2():
#     # app.dependency_overrides[get_current_active_user] = override_dependency_disabled
#     # response_HA_me = client.get("/users/me")
#     # print(response_HA_me)
#     # assert response_HA_me.status_code == 200

#     with patch("signin.get_current_active_user", side_effect=override_dependency_disabled) as mock_get_user:
#         # Now, when client.post is called within this context, it will use the mocked version of get_user_caf_db
#         response = client.get(f"users/me")
#         print(response)

#     assert response.status_code == 200
    
#     # Check if mock_get_user_caf_db was called
#     print(mock_get_user.call_count)  # Debugging statement to check call count
#     assert mock_get_user.call_count == 1  # or any other expected call count










# client = TestClient(app)

# # def override_get_current_user():
# #     return User(username="test", email="test@example.com", disabled=False)



# def test_read_users_me():
#     # app.dependency_overrides[get_current_user] = override_get_current_user
#     with patch('main.get_current_active_user') as mock:
       
#         app.dependency_overrides[get_current_user] = override_dependency_disabled


#         response = client.get("/users/me/")

#         if get_current_user in app.dependency_overrides:
#             print("get_current_user has been overridden")
#         else:
#             print("get_current_user has not been overridden")

#         mock.assert_called_once()
#         assert response.status_code == 400
#     # assert response.json() == {"username": "test", "email": "test@example.com", "disabled": False}

# app.dependency_overrides = {}



# def test_read_users_me(capfd):  # include capfd here
#     app.dependency_overrides[get_current_user] = override_dependency_disabled

#     if get_current_user in app.dependency_overrides:
#         print("get_current_user has been overridden")
#     else:
#         print("get_current_user has not been overridden")

#     response = client.get("/users/me/")

#     # Capture the output
#     captured = capfd.readouterr()
#     print("Captured output:", captured.out)

#     assert response.status_code == 400


#     app.dependency_overrides = {}

# ----------------------------------------------------------------------------------

# def mock_get_current_user():
#     mock_user_disabled = {
#         "username": "tuph01",
#         "full_name": "Kevin Tu",
#         "email": "tuph01@luther.edu",
#         "disabled": True,
#         "student_id": 529194,
#         "hashed_password": "$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm"
#     }
#     user_data = UserInDB(**mock_user_disabled)
#     return user_data
#     # return User(username="mockuser", email="mockuser@example.com", disabled=False)



# def test_read_users_me(monkeypatch):
#     monkeypatch.setattr("signin.get_current_user", mock_get_current_user)
#     response = client.get("/users/me/")
#     print(response)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json() == { "username": "tuph01",
#         "full_name": "Kevin Tu",
#         "email": "tuph01@luther.edu",
#         "disabled": True,
#         "student_id": 529194
#         }



# def mock_get_current_user(token: str):
#     data = {"username": "tuph01",
#         "full_name": "Kevin Tu",
#         "email": "tuph01@luther.edu",
#         "disabled": True,
#         "student_id": 529194,
#         "hashed_password": "$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm"
#     }
#     return UserInDB(**data)

# def test_read_users_me():
#     with patch('main.get_current_active_user') as mock_get_current_active_user:
#         with patch('signin.get_current_user') as mock_get_current_user:
#             with patch('signin.get_current_user', new=mock_get_current_user):
#                 response = client.get("/users/me/")
#                 # assert response.status_code == 200
#                 # assert response.json() == {"username": "mockuser", "email": "mockuser@example.com", "disabled": False}

#                 # Check if get_current_active_user was called
#                 mock_get_current_active_user.assert_called_once()
#                 # Check if get_current_user was called
#                 mock_get_current_user.assert_called_once()

# mock_get_current_user("asdfjk")


# tuph01
# get_user username='tuph01' email='tuph01@luther.edu' full_name='Kevin Tu' disabled=False student_id=529194 hashed_password='$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm'
# get_current_user username='tuph01' email='tuph01@luther.edu' full_name='Kevin Tu' disabled=False student_id=529194 hashed_password='$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm'
# type get_current_user <class 'Assets.jsonFormat.UserInDB'>
# current_active username='tuph01' email='tuph01@luther.edu' full_name='Kevin Tu' disabled=False student_id=529194 hashed_password='$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm'
# <class 'Assets.jsonFormat.UserInDB'>



async def get_current_active_user_disabled_overrride():
    mock_user_disabled = {
        "username": "tuph01",
        "full_name": "Kevin Tu",
        "email": "tuph01@luther.edu",
        "disabled": True,
        "student_id": 529194,
        "hashed_password": "$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm"
    }
    user_data = UserInDB(**mock_user_disabled)

    current_user = user_data

    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def test_authorize_disabled():
    app.dependency_overrides[get_current_active_user] = get_current_active_user_disabled_overrride
    response_HA_me = client.get("/users/me")
    print(response_HA_me.json())
    assert response_HA_me.status_code == 400
    assert response_HA_me.json()["message"] == "disabled user"
