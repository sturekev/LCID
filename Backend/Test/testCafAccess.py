# this is to access main.py
import sys

import pytest
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')

# https://fastapi.tiangolo.com/advanced/testing-dependencies/ 


from fastapi.testclient import TestClient
# from unittest.mock import patch, Mock

from main import app, get_current_active_user, create_caf_swipe_token, getSwipe

sys.path.insert(1, '../Backend/Assets')
from jsonFormat import UserInDB

sys.path.append('../Backend/DiningService')

from DiningService.caf import get_user_caf_db, get_user_dining_db

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()=={"message": "Hello World"}


data = get_user_caf_db("529194") 
print(type(data), data)
print(data["529194"]["swipes"])

user_dining = get_user_dining_db(data, "529194")
print(user_dining)

def mock_get_user_caf_db():
    data = {'529194': {'student_id': '529194', 'swipes': 20, 'dining_dolars': 125.02, 'role': 'Student'}}
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
    response_caf_me = client.get(f"/diningservice/caf/me/{swipes}")
    assert response_caf_me.status_code == 200
    content_response_caf_me = response_caf_me.json()
    assert "message" in content_response_caf_me
    token = content_response_caf_me["message"]
    location = "caf"
    # this should be swipes_left instead of swipes to avoid confusion
    swipes_before = get_user_caf_db("529194")["529194"]["swipes"]

    response = client.post(f"/diningservice/caf/{token}/{location}")
    assert response.status_code == 200
    content_response = response.json()
    # should be 'swipes_left' instead of 'swipes' 
    # to avoid confusion with the amount of times the person want to swipe when entering
    assert content_response["message"] == f"Success {content_response['swipes']}"
    assert content_response["swipes"] == swipes_before - swipes

def test_caf_access_not_enough_swipes():
    app.dependency_overrides[get_current_active_user] = override_dependency_right
    # this should be swipes_left instead of swipes to avoid confusion
    swipes_before = get_user_caf_db("529194")["529194"]["swipes"]
    swipes = swipes_before + 1
    response_caf_me = client.get(f"/diningservice/caf/me/{swipes}")

    #Error 406 is an HTTP status code that indicates that the server cannot satisfy the client's request 
    #because the resource requested by the client has a MEDIA type or format that is not acceptable 
    #according to the preferences specified in the request's "Accept" header.


    # HTTP error code 409, "Conflict," 
    # indicates that the request cannot be completed due to a conflict with the current state of the resource. 
    # Systems may perform integrity checks to ensure that modifications to resources do not violate certain constraints. 
    assert response_caf_me.status_code == 406
    content_response_caf_me = response_caf_me.json()
    assert "detail" in content_response_caf_me
    detail = content_response_caf_me["detail"]
    assert detail == 'Balance not enough'
