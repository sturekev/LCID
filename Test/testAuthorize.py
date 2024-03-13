# this is to access main.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')

# https://fastapi.tiangolo.com/advanced/testing-dependencies/ 


from fastapi.testclient import TestClient

from main import app, get_current_active_user
sys.path.insert(1, '../Backend/Assets')
from jsonFormat import User

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()=={"message": "Hello World"}

async def override_dependency_right():
    mock_user_right = {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "disabled": False,
        "student_id": 529194
    }
    user_data = User(**mock_user_right)
    return user_data

async def override_dependency_disabled():
    mock_user_disabled = {
    "username": "jevin",
    "full_name": "jev Doe",
    "email": "jevdoe@example.com",
    "disabled": True,
    "student_id": 529194
    }
    user_data = User(**mock_user_disabled)
    return user_data
 
def test_authorize_right():
    app.dependency_overrides[get_current_active_user] = override_dependency_right
    response_HA_me = client.get("/HallAccess/me")
    assert response_HA_me.status_code == 200

def test_authorize_disabled():
    app.dependency_overrides[get_current_active_user] = override_dependency_disabled
    response_HA_me = client.get("/HallAccess/me")
    assert response_HA_me.status_code == 409
    
    # print("convoi",response_HA_me.json())
    
# def test_authorize_disabled():
    # pass
