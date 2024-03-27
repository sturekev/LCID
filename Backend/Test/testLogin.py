# this is to access main.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Backend/')
# import main
##################

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_login_right_userpass_all():
    response = client.post("/login/", data={"username": "tuph01", "password": "password3", 
                                            "grant_type":None, "scope":"", 
                                            "client_id":None, "client_secret":None 
                                            })
    assert response.status_code == 200	
    assert "access_token" in response.json()
    
def test_login_right_userpass_2():
    response = client.post("/login/", data={"username": "tuph01", "password": "password3"
                                            })
    assert response.status_code == 200	
    assert "access_token" in response.json()
    
def test_login_wrong_user():
    response = client.post("/login/", data={"username": "khoaitay", "password": "secret"})
    assert response.status_code == 401	
    assert response.json() == {'detail': 'Incorrect username or password'}
    
def test_login_wrong_pass():
    response = client.post("/login/", data={"username": "tuph01", "password": "asdfasdgjagkh"})
    assert response.status_code == 401	
    assert response.json() == {'detail': 'Incorrect username or password'}
    
def test_login_wrong_userpass():
    response = client.post("/login/", data={"username": "convoi", "password": "JKJLKGSDF"})
    assert response.status_code == 401	
    assert response.json() == {'detail': 'Incorrect username or password'}

@pytest.mark.skip("Is disabled account feature still apart of the project?")
def test_login_right_disable():    
    pass
    # response = client.post("/login", data={"username": "jevin", "password": "secret"})
    # assert response.status_code == 409
    # assert response.json() == {'detail': 'Account disabled'}

def test_login_missing_fields1():
    response = client.post("/login/", data={"username": "tuph01"
                                            })
    assert response.status_code == 422
    assert response.json() == {'detail': 'Missing required field(s)'}

def test_login_missing_fields2():
    response = client.post("/login/", data={"password": "password3"
                                            })
    assert response.status_code == 422
    assert response.json() == {'detail': 'Missing required field(s)'}