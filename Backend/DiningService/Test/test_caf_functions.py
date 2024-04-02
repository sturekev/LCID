import sys

sys.path.insert(1, '../Backend')

from DiningService.caf import get_user_caf_db, get_account_id_db, update_user_swipe_db

def test_get_user_caf_db():
    studentId = "528480"
    query_result = get_user_caf_db(studentId)

    assert studentId in query_result
    assert query_result['528480']['student_id'] == '528480'
    assert query_result['528480']['swipes'] == 100
    assert query_result['528480']['dining_dolars'] == 183.89
    assert query_result['528480']['role'] == 'Student'

def test_get_account_id_db():
    studentId = "528480"
    accountId = 1
    query_result = get_account_id_db(studentId)

    assert accountId == query_result

def test_update_user_swipe_db():
    test_student_pk_number = 3
    test_swipes = 3814

    result = update_user_swipe_db(test_student_pk_number, test_swipes)
    assert result == 3814, "The function should return the updated number of swipes."