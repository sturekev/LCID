# this is to access main.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')

# https://fastapi.tiangolo.com/advanced/testing-dependencies/ 


from fastapi.testclient import TestClient

from main import app, get_current_active_user

sys.path.insert(1, '../Backend/Assets')
from jsonFormat import UserInDB

sys.path.append('../Backend/DinningService')
print(sys.path)
from caf import get_user_caf_db

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()=={"message": "Hello World"}

data = get_user_caf_db("529194") 
print(type(data), data)
print(data["529194"]["swipes"])

async def override_user_caf():
    data = {'529194': {'student_id': '529194', 'swipes': 4, 'dining_dolars': 125.02, 'role': 'Student'}}
    return data

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

def test_caf_access_right():
    app.dependency_overrides[get_current_active_user] = override_dependency_right
    swipes = 2
    response_caf_me = client.get(f"/dinningservice/caf/me/{swipes}")
    assert response_caf_me.status_code == 200
    content_response_caf_me = response_caf_me.json()
    assert "message" in content_response_caf_me
    
    token = content_response_caf_me["message"]
    location = "caf"
    response = client.post(f"/dinningservice/caf/{token}/{location}")
    assert response.status_code == 200
    content_response = response.json()
    assert content_response["message"] == "Success"
    assert content_response["success"] == True
    # should be 'swipes_left' instead of 'swipes' 
    # to avoid confusion with the amount of times the person want to swipe when entering
    assert content_response["swipes_left"] == 20-swipes

def test_caf_access_not_enough_swipes():
    app.dependency_overrides[get_current_active_user] = override_dependency_right
    swipes = 21
    response_caf_me = client.get(f"/dinningservice/caf/me/{swipes}")
    assert response_caf_me.status_code == 200
    content_response_caf_me = response_caf_me.json()
    assert "message" in content_response_caf_me
    
    token = content_response_caf_me["message"]
    location = "caf"
    response = client.post(f"/dinningservice/caf/{token}/{location}")
    assert response.status_code == 200
    content_response = response.json()
    assert content_response["message"] == f"Balance not enough for {swipes} swipes"
    assert content_response["success"] == False
    # should be 'swipes_left' instead of 'swipes' 
    # to avoid confusion with the amount of times the person want to swipe when entering
    assert content_response["swipes_left"] == 20

def test_spelling():
    raise ValueError("Spelling Error in main.py and Backend folder: 'DiningService' , not 'DinningService'")
