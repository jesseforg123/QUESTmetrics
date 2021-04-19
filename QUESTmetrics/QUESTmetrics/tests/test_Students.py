import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup


def test_get_empty():
    #Just call this with whatever request you need
    response = GET('/students')
    assert response.status_code == 200
    #NOTE: This JSON isn't in quotes. We can do comparisons with objects.
    assert response.json() == []


def test_simple_post_delete():
    response = POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId&uid=0')
    assert response.status_code == 200
    students = response.json()

    assert students['firstName'] == 'testFirst'
    assert students['lastName'] == 'testLast'
    assert students['directoryId'] == 'testId'
    assert students['uid'] == 0

    DELETE('/student/uid/0')

    test_get_empty()

def test_many_post():
    for i in range(5):
        response = POST('/students?firstName=testFirst{}&lastName=testLast{}&directoryId=testId{}&uid={}'.format(i, i, i, i))
        assert response.status_code == 200
    
    students = GET('/students').json()
    assert len(students) == 5

    for i in range(5):
        assert students[i]['firstName'] == 'testFirst' + str(i)
        assert students[i]['lastName'] == 'testLast' + str(i)
        assert students[i]['directoryId'] == 'testId' + str(i)
        assert students[i]['uid'] == i

        resp = DELETE('/student/uid/{}'.format(i))


def test_duplicate_name():
    POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId&uid=0')
    resp = POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId1&uid=1')
    assert resp.status_code == 200
    students = GET('/students').json()

    assert len(students) == 2
    assert students[0]['firstName'] == students[1]['firstName']
    assert students[0]['lastName'] == students[1]['lastName']

    DELETE('/student/uid/0')
    DELETE('/student/uid/1')


def test_duplicate_directoryid():
    POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId&uid=0')
    resp = POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId&uid=1')

    assert resp.status_code == 400
    students = GET('/students').json()
    assert len(students) == 1

    DELETE('/student/uid=0')

def test_duplicate_uid():
    POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId&uid=0')
    resp = POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId1&uid=0')

    assert resp.status_code == 400
    students = GET('/students').json()
    assert len(students) == 1

    DELETE('/student/uid=0')

def test_missing_name_args():
    resp = POST('/students?directoryId=testId&uid=0')
    assert resp.status_code == 400
    students = GET('/students').json()
    assert len(students) == 0

def test_missing_directoryid_args():
    resp = POST('/students?firstName=testFirst&lastName=testLast&uid=0')
    assert resp.status_code == 400
    students = GET('/students').json()
    assert len(students) == 0

def test_missing_uid_args():
    resp = POST('/students?firstName=testFirst&lastName=testLast&directoryId=testId')
    assert resp.status_code == 200
    students = GET('/students').json()
    assert len(students) == 1

    assert students[0]['uid'] == None

    DELETE('/student/directoryId=testId')


