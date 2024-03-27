import sys
import pytest

from fastapi.testclient import TestClient

sys.path.insert(1, '../Backend/')
sys.path.insert(1, '../Backend/Assets')
# sys.path.append('../Backend/DinningService')
from DinningService.caf import verify_caf_swipe
from db_connection import get_db_connection

from jsonFormat import UserInDB
from main import app, get_current_active_user

client = TestClient(app)

@pytest.fixture(scope="module")
def local_db_connection():
    db_connection = get_db_connection()
    yield db_connection
    db_connection.close()

@pytest.fixture(scope="module")
def aws_db_connection():
    db_connection = get_db_connection()
    yield db_connection
    db_connection.close()

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

def test_local_database_connection_success(local_db_connection):
    cursor = local_db_connection.cursor()
    cursor.execute("SELECT 1")
    assert cursor.fetchone() == (1,), "Local database connection failed"

def test_aws_database_connection_success(aws_db_connection):
    cursor = aws_db_connection.cursor()
    cursor.execute("SELECT 1")
    assert cursor.fetchone() == (1,), "AWS database connection failed"

def test_user_retrieve_one_success(local_db_connection, aws_db_connection):
    local_cursor = local_db_connection.cursor()
    aws_cursor = aws_db_connection.cursor()

    local_cursor.execute('''SELECT fullname, username, password, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    local_result = local_cursor.fetchone()

    aws_cursor.execute('''SELECT fullname, username, password, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    aws_result = aws_cursor.fetchone()

    assert local_result == aws_result, "User does not exist in one of the databases"

def test_user_retrieve_one_success_2(local_db_connection, aws_db_connection):
    local_cursor = local_db_connection.cursor()
    aws_cursor = aws_db_connection.cursor()

    local_cursor.execute('''SELECT fullname, username, password 
                        FROM account
                        WHERE username = 'tuph01' ''')
    local_result = local_cursor.fetchone()

    aws_cursor.execute('''SELECT fullname, username, password 
                        FROM account
                        WHERE username = 'tuph01' ''')
    aws_result = aws_cursor.fetchone()

    assert local_result == aws_result, "User does not exist in one of the databases"

def test_user_retrieve_one_fail(local_db_connection, aws_db_connection):
    local_cursor = local_db_connection.cursor()
    aws_cursor = aws_db_connection.cursor()

    local_cursor.execute('''SELECT fullname, username, password 
                        FROM account
                        WHERE username = 'tuph01' ''')
    local_result = local_cursor.fetchone()

    aws_cursor.execute('''SELECT fullname, username, password 
                        FROM account
                        WHERE username = 'phattu01' ''')
    aws_result = aws_cursor.fetchone()

    assert local_result != aws_result, "Expected Failure: Users do not match in existing databases"

def test_users_retrieve_all_success(local_db_connection, aws_db_connection):
    local_cursor = local_db_connection.cursor()
    aws_cursor = aws_db_connection.cursor()

    local_cursor.execute('''SELECT fullname, username, password, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    local_result = local_cursor.fetchall()

    aws_cursor.execute('''SELECT fullname, username, password, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    aws_result = aws_cursor.fetchall()

    assert local_result == aws_result, "User does not exist in one of the databases"

def test_users_retrieve_all_failure(local_db_connection, aws_db_connection):
    local_cursor = local_db_connection.cursor()
    aws_cursor = aws_db_connection.cursor()

    local_cursor.execute('''SELECT username, password, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    local_result = local_cursor.fetchall()

    aws_cursor.execute('''SELECT fullname, username, password, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    aws_result = aws_cursor.fetchall()

    assert local_result != aws_result, "User does not exist in one of the databases"

def test_meal_swipe_updated():
    app.dependency_overrides[get_current_active_user] = override_dependency_right
    swipes = 2
    response_caf_me = client.get(f"/dinningservice/caf/me/{swipes}")
    assert response_caf_me.status_code == 200

def test_meal_swipe_not_updated():
    ...

