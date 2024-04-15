
import requests
import jwt
import datetime
def send_data1(token):
    # Your secret key to sign the token. Keep it secret!
    SECRET_KEY = "60528e0f7a9ae5946ddasdd2d012f3904ccf2c7vbe227zxcv79b300095855b429b61303"
    base_url = "http://18.215.231.250"  # Replace with the actual URL of your FastAPI server

    response1 = requests.get(f"{base_url}/echo/{token}")
#  Print the response from the server
    # print("response1")
    # print(response1)
    try: print(response1.json()["enter_time"])
    except: pass    
    # print(response1.json()["message"])
    try:
        return response1.json()["message"]
    except:
        return f"Error, server returned {response1}"

