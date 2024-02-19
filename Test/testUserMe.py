# this is to access main.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')

from fastapi.testclient import TestClient

from main import app, get_current_active_user

sys.path.insert(1, '../Backend/Authenticate')
from signin import get_current_user, get_current_active_user

sys.path.insert(1, '../Backend/Assets')
from jsonFormat import User, UserInDB

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()=={"message": "Hello World"}


async def override_dependency_right():
    mock_user = {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "disabled": False,
        "student_id": 529194
    }
    
    user_data = User(**mock_user)
    return user_data

async def override_dependency_disabled():
    mock_user_disabled = {
        "username": "jevin",
        "full_name": "jev Doe",
        "email": "jev@example.com",
        "disabled": True,
        "student_id" : 529194
    }
    user_data = User(**mock_user_disabled)
    return user_data
    # return mock_user_disabled
    # return UserInDB(**mock_user_disabled)


def test_user_me_right():
    app.dependency_overrides[get_current_active_user] = override_dependency_right
    ## should me "user" not userS !!!!!!!!!!!!!!!!!!!!!!!!!
    response = client.get("/users/me")
    assert response.status_code == 200
    
    response = response.json()
    assert "username" in response
    assert "email" in response
    assert "full_name" in response
    assert "disabled" in response
    assert "student_id" in response
    
def test_user_me_disabled():
    get_current_active_user.dependency_overrides[get_current_user] = override_dependency_disabled
    ## should me "user" not userS !!!!!!!!!!!!!!!!!!!!!!!!!
    response = client.get("/users/me")
    # assert response.status_code == 409
    assert response.status_code == 400
    # message = response.json()["message"]
    message = response.json()

    assert message == "detail: Account Disabled"