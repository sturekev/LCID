# this is to access main.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')

# https://fastapi.tiangolo.com/advanced/testing-dependencies/ 

"""
what: test if authorize (login) feature works
how: if client.get("/HallAccess/me") returns code==200 means the authorize feature works
"""

from fastapi.testclient import TestClient
import pytest

from main import app, get_current_active_user, authenticate_user
sys.path.insert(1, '../Backend/Assets')
from jsonFormat import UserInDB, User

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()=={"message": "Hello World"}

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
    response_HA_me = client.get("/HallAccess/me")
    assert response_HA_me.status_code == 200

@pytest.mark.skip("Is disabled account feature still apart of the project?")
def test_authorize_disabled():
    app.dependency_overrides[get_current_active_user] = override_dependency_disabled
    response_HA_me = client.get("/HallAccess/me")
    assert response_HA_me.status_code == 409
    assert response_HA_me.json() == {'detail': 'Account disabled'}

