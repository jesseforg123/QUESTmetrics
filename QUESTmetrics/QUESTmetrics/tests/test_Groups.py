import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_get_empty():
    response = GET('/groups')
    assert response.status_code == 200
    assert response.json() == []

def test_post_delete_basic():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    response = GET('/groups')
    assert response.status_code == 200
    groups = response.json()
    assert groups[0]["name"] == "test_group"
    assert len(groups) == 1

    response = DELETE('/groups?name=test_group')
    assert response.status_code == 204
    
    response = GET('/groups')
    assert len(response.json()) == 0


def test_post_duplicate():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    response =  POST('/groups?name=test_group&className=test_class&channel=test_channel')

    assert response.status_code == 400
    response = GET('/groups')
    groupList = response.json()
    assert len(groupList) == 1


def test_post_missing_args():
    response = POST('/groups')
    assert response.status_code == 400

    res = GET('/groups')
    assert res.status_code == 200
    assert res.json() == []

def test_post_group_from_bad_class():
    POST('/classes?className=test_class')
    response = POST('/groups?name=test_group&className=not_test_class&channel=test_channel')
    assert response.status_code == 404

def test_delete_propagate():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    response = DELETE('/groups?name=test_group')
    assert response.status_code == 204
    
    response = GET('/slackData/group/test_group')
    assert response.status_code == 404
