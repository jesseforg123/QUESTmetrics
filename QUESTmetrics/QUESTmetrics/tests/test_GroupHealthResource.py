import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup


def test_health_group_dne():
    resp = GET('/group/health/testGroup')
    assert resp.status_code == 404

def test_default_health_is_3():
    POST('/classes?className=testClass')
    POST('/groups?name=testGroup&className=testClass&channel=testChannel')

    resp = GET('/group/health/testGroup')
    assert resp.status_code == 200
    assert resp.json()['result'] == 3

def test_update_health_arg():
    POST('/classes?className=testClass')
    POST('/groups?name=testGroup&className=testClass&channel=testChannel')

    resp = PUT('/group/health/testGroup?groupHealth=2')
    assert resp.status_code == 204
    health = GET('/group/health/testGroup')

    assert health.status_code == 200
    assert health.json()['result'] == 2


def test_put_invalid_health_arg():
    DELETE('/clear')

    POST('/classes?className=testClass')
    POST('/groups?name=testGroup&className=testClass&channel=testChannel')

    resp = PUT('/group/health/testGroup?groupHealth=0')
    assert resp.status_code == 400
    resp = PUT('/group/health/testGroup?groupHealth=4')
    assert resp.status_code == 400
    resp = PUT('/group/health/testGroup?groupHealth=-10')
    assert resp.status_code == 400





