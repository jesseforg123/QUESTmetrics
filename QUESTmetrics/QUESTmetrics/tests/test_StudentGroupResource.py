import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_get_group_dne():
    resp = GET('/students/group/testGroup')
    assert resp.status_code == 404


def test_get_empty_group():
    POST('/classes?className=testClass')
    POST('/groups?name=testGroup&className=testClass&channel=testChannel')
    resp = GET('/students/group/testGroup')
    assert resp.status_code == 200
    assert resp.json() == []

def test_single_add():
    POST('/classes?className=testClass')
    POST('/groups?name=testGroup&className=testClass&channel=testChannel')
    POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId&uid=0')
    POST('/student/directoryId/testId/group/testGroup')

    resp = GET('/students/group/testGroup')
    assert resp.status_code == 200
    students = resp.json()

    assert len(students) == 1
    assert students[0]['firstName'] == 'testFirst'
    assert students[0]['lastName'] == 'testLast'
    assert students[0]['directoryId'] == 'testId'
    assert students[0] ['uid'] == 0