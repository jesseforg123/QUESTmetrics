import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup
# POST AND DELETE
# Add a student (from uid) to a group (with groupname)
# /student/uid/<uid>/group/<groupName>


def test_post_basic():
    DELETE('/clear')
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = POST('/student/uid/0/group/test_group')
    assert response.status_code == 200

    response = GET('/students/group/test_group')
    group = response.json()
    group[0]["uid"] == 0
    assert response.status_code == 200

def test_post_bad_group():
    DELETE('/clear')
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = POST('/student/uid/0/group/not_test_group')
    assert response.status_code == 404

def test_post_bad_uid():
    DELETE('/clear')
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = POST('/student/uid/1/group/test_group')
    assert response.status_code == 404

def test_post_delete_basic():
    DELETE('/clear')
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = POST('/student/uid/0/group/test_group')
    assert response.status_code == 200
    group = response.json()

    response = GET('/students/group/test_group')
    assert response.status_code == 200

    response = DELETE('/student/uid/0/group/test_group')
    assert response.status_code == 204

def test_post_delete_bad_group():
    DELETE('/clear')
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = POST('/student/uid/0/group/test_group')
    assert response.status_code == 200
    group = response.json()

    response = DELETE('/student/uid/0/group/not_test_group')
    assert response.status_code == 404
    len(group) == 1

    response = DELETE('/student/uid/0/group/test_group')
    assert response.status_code == 204
    len(group) == 0


def test_post_delete_bad_uid():
    DELETE('/clear')
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = POST('/student/uid/0/group/test_group')
    assert response.status_code == 200
    group = response.json()

    response = DELETE('/student/uid/1/group/test_group')
    assert response.status_code == 404
    len(group) == 1

    response = DELETE('/student/uid/0/group/test_group')
    assert response.status_code == 204
    len(group) == 0

def test_data_propagate():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    POST('/student/uid/0/group/test_group')

    #ELMS Data was inserted
    assert GET('/elmsData/student/uid/0/class/test_class').status_code == 200

    DELETE('/student/uid/0/group/test_group')

    #ELMS Data was deleted
    assert GET('/elmsData/student/uid/0/class/test_class').status_code == 404
