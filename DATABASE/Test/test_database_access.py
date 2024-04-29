import pytest

from db_connection import get_db_connection, get_aws_db_connection


@pytest.fixture(scope="module")
def local_db_connection():
    db_connection = get_db_connection()
    yield db_connection
    db_connection.close()

@pytest.fixture(scope="module")
def aws_db_connection():
    db_connection = get_aws_db_connection()
    yield db_connection
    db_connection.close() 

def test_aws_database_connection_success(aws_db_connection):
    cursor = aws_db_connection.cursor()
    cursor.execute("SELECT 1")
    assert cursor.fetchone() == (1,), "AWS database connection failed"

def test_user_retrieve_one_success(local_db_connection, aws_db_connection):
    aws_cursor = aws_db_connection.cursor()

    expected_result = ('Samuel Vue', 'vuesa01', '528480', 'Farwell')
    
    aws_cursor = aws_db_connection.cursor()
    aws_cursor.execute('''SELECT fullname, username, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    aws_result = aws_cursor.fetchone()

    assert expected_result == aws_result, "User does not exist in one of the databases"

def test_user_retrieve_one_success_2(local_db_connection, aws_db_connection):
    aws_cursor = aws_db_connection.cursor()
    
    expected_result = ('Kevin Tu', 'tuph01')
    
    aws_cursor.execute('''SELECT fullname, username 
                        FROM account
                        WHERE username = 'tuph01' ''')
    aws_result = aws_cursor.fetchone()
    
    assert expected_result == aws_result, "User does not exist in one of the databases"

def test_user_retrieve_one_fail(local_db_connection, aws_db_connection):
    aws_cursor = aws_db_connection.cursor()

    aws_cursor.execute('''SELECT fullname, username 
                        FROM account
                        WHERE username = 'phattu01' ''')
    aws_result = aws_cursor.fetchone()

    assert [] != aws_result, "Expected Failure: Users do not match in existing databases"

def test_users_retrieve_all_success(local_db_connection, aws_db_connection):
    aws_cursor = aws_db_connection.cursor()
    
    expected_result = [('Samuel Vue', 'vuesa01', '528480', 'Farwell'), ('Reece Flynn', 'flynre01', '527836', 'College Apartments'), ('Kevin Tu', 'tuph01', '529194', 'Miller')]
    
    aws_cursor.execute('''SELECT fullname, username, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    aws_result = aws_cursor.fetchall()
    
    assert expected_result == aws_result, "User does not exist in one of the databases"

def test_users_retrieve_all_failure(local_db_connection, aws_db_connection):
    aws_cursor = aws_db_connection.cursor()
    aws_cursor.execute('''SELECT fullname, username, id_number, building_name 
                        FROM account, account_profile, building_info 
                        WHERE account_profile.account_id = account.id 
                        AND building_info.building_id = account_profile.housing''')
    aws_result = aws_cursor.fetchall()

    assert [] != aws_result, "User does not exist in one of the databases"
