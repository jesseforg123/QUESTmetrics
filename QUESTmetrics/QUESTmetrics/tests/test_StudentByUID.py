import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

# TESTS GET AND DELETE

# GET: GETS PERSON GIVEN UID
# DELETE: DELETES PERSON GIVEN UID FROM STUDENT TABLE

# GET TESTS
def test_get_bad_UID():
    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')

    response = GET('/student/uid/1')
    assert response.status_code == 404

def test_get_bad_UID_letters():
    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')

    response = GET('/student/uid/a')
    assert response.status_code == 400

def test_get_good_UID():

    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')

    response = GET('/student/uid/0')
    assert response.status_code == 200

def test_get_bad_UID_in_group():

    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')
    POST('/student/uid/0/group/test_group')

    response = GET('/student/uid/1')
    assert response.status_code == 404

def test_get_good_UID_in_group():

    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')
    POST('/student/uid/0/group/test_group')

    response = GET('/student/uid/0')
    assert response.status_code == 200

# DELETE TESTS
def test_delete_bad_UID():

    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')

    response = DELETE('/student/uid/1')
    assert response.status_code == 404

def test_delete_good_UID():

    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')

    response = DELETE('/student/uid/0')
    assert response.status_code == 204

    response = GET('/student/uid/0')
    assert response.status_code == 404

def test_delete_bad_UID_letters():

    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')

    response = DELETE('/student/uid/a')
    assert response.status_code == 400


def test_delete_missing_arg():

    response = DELETE('/student/uid')
    assert response.status_code == 404

def test_delete_bad_UID_in_group():

    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')
    POST('/student/uid/0/group/test_group')

    response = DELETE('/student/uid/1')
    assert response.status_code == 404

def test_delete_good_UID_in_group():

    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')
    POST('/student/uid/0/group/test_group')

    response = GET('/student/uid/0')
    assert response.status_code == 200

    response = DELETE('/student/uid/0')
    assert response.status_code == 204

    response = GET('/student/uid/0')

    assert response.status_code == 404

def test_data_propagate():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    POST('/student/directoryId/test_directory_id/group/test_group')

    #ELMS Data was inserted
    assert GET('/elmsData/student/uid/0/class/test_class').status_code == 200

    DELETE('/student/uid/0')

    #ELMS Data was deleted
    assert GET('/elmsData/student/uid/0/class/test_class').status_code == 404
