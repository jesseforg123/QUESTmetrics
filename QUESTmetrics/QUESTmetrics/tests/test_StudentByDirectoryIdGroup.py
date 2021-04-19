import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_post_delete_basic():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = POST('/student/directoryId/test_directory_id/group/test_group')
    assert response.status_code == 200

    response = GET('/students/group/test_group')
    assert len(response.json()) == 1

    response = DELETE('/student/directoryId/test_directory_id/group/test_group')
    assert response.status_code == 204

    response = GET('/students/group/test_group')
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_post_deleted_student():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    DELETE('/student/directoryId/test_directory_id')

    response = POST('/group/test_group/student/directoryId/test_directory_id')
    assert response.status_code == 404

def test_post_bad_directoryId():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    response = POST('/group/test_group/student/directoryId/not_a_student')
    assert response.status_code == 404

def test_post_bad_group():
    POST('/classes?className=test_class')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = POST('/group/not_a_group/student/directoryId/test_directory_id')
    assert response.status_code == 404

def test_post_duplicate():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = POST('/student/directoryId/test_directory_id/group/test_group')
    assert response.status_code == 200

    response = POST('/student/directoryId/test_directory_id/group/test_group')
    assert response.status_code == 400

    response = GET('/students/group/test_group')
    assert len(response.json()) == 1

def test_delete_bad_directoryId():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    response = DELETE('/group/test_group/student/directoryId/not_a_student')
    assert response.status_code == 404

def test_delete_bad_group():
    POST('/classes?className=test_class')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    response = DELETE('/group/not_a_group/student/directoryId/test_directory_id')
    assert response.status_code == 404

def test_data_propagate():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    POST('/student/uid/0/group/test_group')

    #ELMS Data was inserted
    assert GET('/elmsData/student/uid/0/class/test_class').status_code == 200

    DELETE('/student/directoryId/test_directory_id/group/test_group')

    #ELMS Data was deleted
    assert GET('/elmsData/student/uid/0/class/test_class').status_code == 404


