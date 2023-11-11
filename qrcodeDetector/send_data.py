
## biến thành function


import requests
import jwt
import datetime
# def abcd():
#     # Define the base URL of your FastAPI server
#     base_url = "http://127.0.0.1:8000"  # Replace with the actual URL of your FastAPI server

#     # Define the message you want to send
#     message = "convoi"

#     # Example using a GET request with a path parameter
#     response1 = requests.get(f"{base_url}/echo/{message}")

#     # Example using a POST request with a request body
#     data = {"message": message}
#     response2 = requests.post(f"{base_url}/receive_message/", json=data)

#     # Print the response from the server
#     print("response1")
#     print(response1.status_code)
#     print(response1.json())

#     print("response2")
#     print(response2.status_code)
#     print(response2.json())

def abcd():
    # Your secret key to sign the token. Keep it secret!
    SECRET_KEY = "60528e0f7a9ae5946ddasdd2d012f3904ccf2c7vbe227zxcv79b300095855b429b61303"
    base_url = "http://127.0.0.1:8000"  # Replace with the actual URL of your FastAPI server

    # Data you want to encode into the token
    payload = {
        "user_id": 123,
        "username": "john_doe",
        "caf_swipes_left":7,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=200)  # Token expiration time
    }

    # Encode the data into a JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    print(token)
    # print(payload["exp"],type(payload["exp"]))
    # print("Encoded JWT token:", token)
    # print("type",type(token))
    
    response1 = requests.get(f"{base_url}/echo/{token}")
#  Print the response from the server
    # print("response1")
    # print(response1.status_code)
    try: print(response1.json()["enter_time"])
    except: pass    
    print(response1.json()["message"])
abcd()
