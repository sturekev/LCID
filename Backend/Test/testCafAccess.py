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

# @pytest.mark.asyncio
# async def test_caf_access_mock():
#     swipes = 2
#     with patch("main.create_caf_swipe_token", side_effect = mock_get_user_caf_db):
#         response = await getSwipe(swipes, current_user=mock_get_user_caf_db)
#         print(response)
#         assert response["message"] == "mocked_token"
#         assert response["token_type"] == "Bearer"

# @pytest.mark.asyncio
# async def test_caf_access_mock():
#     swipes = 2
#     # Mocking the dependency function
#     mock_user = Mock(student_id='529194')
#     response = await getSwipe(swipes, current_user=mock_user)
#     print("convoi",response)
#     with patch("main.create_caf_swipe_token", side_effect=mock_get_user_caf_db):
#         # Creating a mock User object with necessary attributes
#         mock_user = Mock(student_id='529194')
#         print(mock_user)
#         response = await getSwipe(swipes, current_user=mock_user)
#         print(response)
#         assert response["message"] == "mocked_token"
#         # assert response["token_type"] == "Bearer"

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

    
#     with patch("caf.get_user_caf_db", side_effect=mock_get_user_caf_db):
#         print(mock_get_user_caf_db())
#         print(get_user_caf_db())
#         response = client.post(f"/diningservice/caf/{token}/{location}")
#         assert response.status_code == 200
#         content_response = response.json()
#         assert content_response["swipes"] == True
#         assert content_response["message"] == "Success"
#         # should be 'swipes_left' instead of 'swipes' 
#         # to avoid confusion with the amount of times the person want to swipe when entering
#         assert content_response["swipes_left"] == 20-swipes

    response = client.post(f"/diningservice/caf/{token}/{location}")
    assert response.status_code == 200
    content_response = response.json()
    # should be 'swipes_left' instead of 'swipes' 
    # to avoid confusion with the amount of times the person want to swipe when entering
    assert content_response["message"] == f"Success {content_response['swipes']}"
    assert content_response["swipes"] == swipes_before - swipes



# def test_caf_access_not_enough_swipes():
#     app.dependency_overrides[get_current_active_user] = override_dependency_right
#     swipes = 21
#     response_caf_me = client.get(f"/diningservice/caf/me/{swipes}")
#     assert response_caf_me.status_code == 200
#     content_response_caf_me = response_caf_me.json()
#     assert "message" in content_response_caf_me
    
#     token = content_response_caf_me["message"]
#     location = "caf"
#     response = client.post(f"/diningservice/caf/{token}/{location}")
#     assert response.status_code == 200
#     content_response = response.json()
#     assert content_response["message"] == f"Balance not enough for {swipes} swipes"
#     assert content_response["success"] == False
#     # should be 'swipes_left' instead of 'swipes' 
#     # to avoid confusion with the amount of times the person want to swipe when entering
#     assert content_response["swipes_left"] == 20

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



# def test_spelling():
#     raise ValueError("Spelling Error in main.py and Backend folder: 'DiningService' , not 'diningservice'")





# from unittest.mock import patch

# def test_caf_access_right():
#     app.dependency_overrides[get_current_active_user] = override_dependency_right
#     swipes = 2
#     response_caf_me = client.get(f"/diningservice/caf/me/{swipes}")
#     assert response_caf_me.status_code == 200
#     content_response_caf_me = response_caf_me.json()
#     assert "message" in content_response_caf_me

#     token = content_response_caf_me["message"]
#     location = "caf"

#     # Patching get_user_caf_db within the context where client.post is called
#     with patch("caf.get_user_caf_db", side_effect=mock_get_user_caf_db) as mock_get_user:
#         # Now, when client.post is called within this context, it will use the mocked version of get_user_caf_db
#         response = client.post(f"/diningservice/caf/{token}/{location}")

#     assert response.status_code == 200
    
#     # Check if mock_get_user_caf_db was called
#     print(mock_get_user.call_count)  # Debugging statement to check call count
#     assert mock_get_user.call_count == 1  # or any other expected call count

