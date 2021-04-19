import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_get_bad_class():
    response = GET('/groups/class/not_a_class')
    assert response.status_code == 404

def test_get_empty():
    POST('/classes?className=test_class')

    response = GET('/groups/class/test_class')
    assert response.status_code == 200
    assert response.json() == []

def test_get_basic():
    POST('/classes?className=test_class')
    
    POST('/groups?name=test_group1&className=test_class&channel=test_channel1')
    POST('/groups?name=test_group2&className=test_class&channel=test_channel2')

    response = GET('/groups/class/test_class')

    assert response.status_code == 200
    assert len(response.json()) == 2