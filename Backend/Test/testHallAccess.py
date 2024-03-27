# this is to access main.py
import sys
from freezegun import freeze_time
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')


from fastapi.testclient import TestClient

from main import app, get_current_active_user
sys.path.insert(1, '../Backend/Assets')
from jsonFormat import UserInDB

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()=={"message": "Hello World"}


async def override_dependency():
    mock_user = {
       "username": "tuph01",
        "full_name": "Kevin Tu",
        "email": "tuph01@luther.edu",
        "disabled": False,
        "student_id": 529194,
        "hashed_password": "$2b$12$pzXAzMq09IhPZjcJ7c.xq.vdJ4dE7307BlJAUBh7G2pzKAd4NfjEm"
    }
    
    user_data = UserInDB(**mock_user)
    return user_data
        
def get_HA_token_from_HA_me():
    app.dependency_overrides[get_current_active_user] = override_dependency
    response_HA_me = client.get("/HallAccess/me")
    assert response_HA_me.status_code == 200
    return response_HA_me.json()["message"]
    
# https://fastapi.tiangolo.com/advanced/testing-dependencies/ 
def test_HallAccess_right_before23():
    hall_access_token = get_HA_token_from_HA_me()
    hall_name = "Miller"
    with freeze_time("2024-01-14 11:35:15"):
        response2 = client.post(f"/HallAccess/{hall_name}/{hall_access_token}")
        assert response2.status_code == 200
        assert response2.json()=={"message": True}

def test_HallAccess_right_after23():
    hall_access_token = get_HA_token_from_HA_me()
    hall_name = "Miller"
    with freeze_time("2024-01-14 00:35:15"):
        response2 = client.post(f"/HallAccess/{hall_name}/{hall_access_token}")
        assert response2.status_code == 200
        assert response2.json()=={"message": True}
        
def test_HallAccess_wrong_token_before23():
    hall_access_token = "dkfjhaskdjhgkjhgasdgkljasdtlfasdga"
    hall_name = "Miller"
    with freeze_time("2024-01-14 11:35:15"):
        response2 = client.post(f"/HallAccess/{hall_name}/{hall_access_token}")
        assert response2.status_code == 401
        
def test_HallAccess_wrong_token_after23():
    hall_access_token = "dkfjhaskdjhgkjhgasdgkljasdtlfasdga"
    hall_name = "Miller"
    with freeze_time("2024-01-14 02:35:15"):
        response2 = client.post(f"/HallAccess/{hall_name}/{hall_access_token}")
        # print("print, convoi", response2.status_code)
        assert response2.status_code == 401
# why is it sometimes 401 sometimes False???? ##############################

def test_HallAccess_nonexist_hall():
    hall_access_token = get_HA_token_from_HA_me()
    hall_name = "asdkgjlaksdgj"
    response2 = client.post(f"/HallAccess/{hall_name}/{hall_access_token}")
    # print(response2.json())
    assert response2.status_code == 404

# HALL_ACCESS should only be denied after 11pm  
# needs 2 test cases: before & after 23pm ########################################

def test_HallAccess_wrong_hall_before23():
    hall_access_token = get_HA_token_from_HA_me()
    hall_name = "Brandt"
    with freeze_time("2024-01-14 12:00:01"):
        response2 = client.post(f"/HallAccess/{hall_name}/{hall_access_token}")
        assert response2.status_code == 200
        assert response2.json()=={"message": True}

def test_HallAccess_wrong_hall_after23():
    hall_access_token = get_HA_token_from_HA_me()
    hall_name = "Brandt"
    with freeze_time("2024-01-14 00:01:13"):
        response2 = client.post(f"/HallAccess/{hall_name}/{hall_access_token}")
        assert response2.status_code == 200
        assert response2.json()=={"message": False}
    
    
