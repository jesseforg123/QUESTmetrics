import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_get_bad_uid():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    response = GET('/groups/student/uid/0')
    assert response.status_code == 404

def test_one_group():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    POST('/student/uid/0/group/test_group')
    response = GET('/groups/student/uid/0')
    assert response.status_code == 200
    len(response.json()) == 1

def test_two_groups():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    POST('/student/uid/0/group/test_group')

    POST('/classes?className=test_class2')
    POST('/groups?name=test_group2&className=test_class2&channel=test_channel2')
    POST('/student/uid/0/group/test_group2')

    response = GET('/groups/student/uid/0')
    assert response.status_code == 200
    len(response.json()) == 2
