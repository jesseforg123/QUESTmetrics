import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_belongs_to_no_groups():
    POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId&uid=0')

    resp = GET('/groups/student/directoryId/testId')
    assert resp.status_code == 200
    assert resp.json() == []

def test_student_dne():

    resp = GET('/groups/student/directoryId/testId')

    assert resp.status_code == 404

def test_student_in_one_group():
    POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId&uid=0')
    POST('/classes?className=testClass')
    POST('/groups?name=testGroup&className=testClass&channel=testChannel')

    POST('/student/uid/0/group/testGroup')

    resp = GET('/groups/student/directoryId/testId')
    assert resp.status_code == 200

    assert resp.json()[0]['name'] == 'testGroup'
    assert len(resp.json()) == 1

def test_student_in_many_groups():
    POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId&uid=0')
    POST('/classes?className=testClass')
    POST('/groups?name=testGroup&className=testClass&channel=testChannel')
    POST('/groups?name=testGroup2&className=testClass&channel=testChannel2')
    POST('/groups?name=testGroup3&className=testClass&channel=testChannel3')


    POST('/student/uid/0/group/testGroup')
    POST('/student/uid/0/group/testGroup2')
    POST('/student/uid/0/group/testGroup3')


    resp = GET('/groups/student/directoryId/testId')

    assert resp.status_code == 200
    groups = resp.json()

    assert len(groups) == 3
    assert groups[0]['name'] == 'testGroup'
    assert groups[1]['name'] == 'testGroup2'
    assert groups[2]['name'] == 'testGroup3'