import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_get_bad_directoryId():
    DELETE('/clear')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    response = GET('/student/directoryId/111')

    assert response.status_code == 404

def test_get_good_directoryId():
    DELETE('/clear')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    response = GET('/student/directoryId/test_directory_id')
    print(response.text)

    assert response.status_code == 200


def test_get_after_delete():
    DELETE('/clear')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    DELETE('/student/uid/0')
    response = GET('/student/directoryId/test_directory_id')

    assert response.status_code == 404

def test_good_delete_directoryId():
    DELETE('/clear')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    response = DELETE('/student/directoryId/test_directory_id')
    assert response.status_code == 204

def test_bad_delete_directoryId():
    DELETE('/clear')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')
    response = DELETE('/student/directoryId/test_dire')
    assert response.status_code == 404

def test_good_delete_group():
    DELETE('/clear')
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')
    POST('/student/uid/0/group/test_group')
    response = DELETE('/student/directoryId/test_directoryId')
    assert response.status_code == 204

    response = GET('/student/directoryId/test_directoryId')
    assert response.status_code == 404


def test_bad_delete_group():
    DELETE('/clear')
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')
    POST('/student/uid/0/group/test_group')


    response = DELETE('/student/directoryId/test_dire')
    assert response.status_code == 404


def test_double_delete_directoryId():
    DELETE('/clear')
    POST('/students?firstName=test_first_name&lastName=test_last_name&directoryId=test_directoryId&uid=0')
    response = DELETE('/student/directoryId/test_directoryId')
    assert response.status_code == 204

    response = GET('/student/directoryId/test_directoryId')
    assert response.status_code == 404

    response = DELETE('/student/directoryId/test_directoryId')
    assert response.status_code == 404

def test_post_basic():
    DELETE('/clear')
    POST('/students?firstName=test_first_name&lastName=test_name&directoryId=test_directoryId&uid=0')

    DELETE('/student/directoryId/test_directoryId')

    response = GET('/student/directoryId/test_directoryId')
    assert response.status_code == 404

    response = POST('/student/directoryId/test_directoryId?uid=0')
    assert response.status_code == 200
    response = GET('/student/directoryId/test_directoryId')
    assert response.status_code == 200

def test_post_already_student():
    DELETE('/clear')
    POST('/students?firstName=test_first_name&lastName=test_name&directoryId=test_directoryId&uid=0')

    response = POST('/student/directoryId/test_directoryId?uid=0')
    assert response.status_code == 400

    response = GET('/student/directoryId/test_directoryId')
    assert response.status_code == 200

    response = GET('/students')


def test_post_not_a_person():
    DELETE('/clear')
    response = POST('/student/directoryId/not_a_person')
    assert response.status_code == 404

def test_data_propagate():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    POST('/students?firstName=test_firstName&lastName=test_lastName&directoryId=test_directory_id&uid=0')

    POST('/student/directoryId/test_directory_id/group/test_group')

    #ELMS Data was inserted
    assert GET('/elmsData/student/uid/0/class/test_class').status_code == 200

    DELETE('/student/directoryId/test_directory_id')

    #ELMS Data was deleted
    assert GET('/elmsData/student/uid/0/class/test_class').status_code == 404