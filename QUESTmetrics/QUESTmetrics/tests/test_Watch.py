import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_get_good_watch():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    response = GET('/group/watch/test_group')

    assert response.status_code == 200


def test_get_bad_watch():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    response = GET('/group/watch/test_gr')

    assert response.status_code == 404

def test_post_good_watch():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    response = POST('/group/watch/test_group')

    assert response.status_code == 204

def test_post_bad_watch():
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')
    response = POST('/group/watch/test_gro')

    assert response.status_code == 404
