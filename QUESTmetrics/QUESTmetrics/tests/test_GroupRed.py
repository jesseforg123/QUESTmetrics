import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_no_groups():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    response = GET('/groups/red')
    assert response.status_code == 200
    assert response.json() == []



def test_red_groups():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    PUT('/group/health/test_group?groupHealth=1')

    response = GET('/groups/red')
    assert response.status_code == 200
    assert len(response.json()) == 1
