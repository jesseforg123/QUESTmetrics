import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_get_good_group():
    POST('/classes?className=test_class')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/student/uid/0/group/test_group')

    response = GET('/elmsData/student/uid/0/class/test_class')
    assert response.status_code == 200

def test_get_bad_group():
    POST('/classes?className=test_class')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/student/uid/0/group/test_group')

    response = GET('/elmsData/student/uid/0/class/not_a_class')
    assert response.status_code == 404

def test_get_bad_table():
    POST('/classes?className=test_class')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/student/uid/0/group/test_group')

    response = GET('/not_a_table/student/uid/0/class/test_class')
    assert response.status_code == 404

def test_get_empty():
    POST('/classes?className=test_class')
    response = POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/student/uid/0/group/test_group')

    response = GET('/elmsData/student/uid/0/class/test_class')
    assert response.status_code == 200
    assert response.json() is not None and response.json()['result'] == ""

def test_put_bad_file():
    POST('/classes?className=test_class')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/student/uid/0/group/test_group')

    #No file
    response = PUT('/elmsData/student/uid/0/class/test_class')
    assert response.status_code == 400

    response = GET('/elmsData/student/uid/0/class/test_class')
    assert response.status_code == 200
    assert response.json() is not None and response.json()['result'] == ""

    #Misnamed file
    response = response = PUT('/elmsData/student/uid/0/class/test_class',
     file='files/messages.csv', attachment_name='bad_name')
    assert response.status_code == 400

    response = GET('/elmsData/student/uid/0/class/test_class')
    assert response.status_code == 200
    assert response.json() is not None and response.json()['result'] == ""

def test_put_bad_group():
    POST('/classes?className=test_class')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/student/uid/0/group/test_group')

    response = GET('/elmsData/student/uid/0/class/not_a_class')
    assert response.status_code == 404

def test_put_bad_table():
    POST('/classes?className=test_class')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/student/uid/0/group/test_group')

    response = PUT('/not_a_table/student/uid/0/class/test_class')
    assert response.status_code == 404

def test_put_get_basic():
    # POST('/classes?className=test_class')
    # POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    # POST('/groups?name=test_group&className=test_class&channel=test_channel')
    # POST('/student/uid/0/group/test_group')

    response = POST('/elmsData/student/uid/0/class/test_class?filePath=Users/stschoberg/Desktop/435/questmetrics/QUESTmetrics/tests/files/elms_data.csv')
    assert response.status_code == 204

    response = GET('/elmsData/student/uid/0/class/test_class')
    assert response.status_code == 200

    assert response.json() is not None
    assert response.json()['result'] == true_file
