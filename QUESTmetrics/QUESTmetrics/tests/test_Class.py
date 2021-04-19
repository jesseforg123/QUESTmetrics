import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup


def test_get_empty():
    #Just call this with whatever request you need
    response = GET('/classes')
    assert response.status_code == 200
    #NOTE: This JSON isn't in quotes. We can do comparisons with objects.
    assert response.json() == []

def test_post_delete():
    #NOTE: the format to make a query and how I call the item test_class. Every test class added and removed should be called that.
    POST('/classes?className=test_class')

    response = GET('/classes')
    assert response.status_code == 200
    classList = response.json()
    assert classList[0]["className"] == "test_class"

    DELETE('/classes?className=test_class')
    response = GET('/classes')
    assert response.json() == []

def test_post_duplicate():
    POST('/classes?className=test_class')
    response = POST('/classes?className=test_class')

    assert response.status_code == 400
    response = GET('/classes')
    classList = response.json()
    assert len(classList) == 1

def test_post_missing_required_args():
    response = POST('/classes')
    assert response.status_code == 400

    response = GET('/classes')
    assert response.json() == []

def test_delete_bad_class():
    response = GET('/classes')
    pre = len(response.json())

    response = DELETE('/classes?className=not_a_class')
    assert response.status_code == 404

def test_delete_propagate():
    #Create class
    POST('/classes?className=test_class')
    #Create group in this class
    response = POST('/groups?name=test_group&className=test_class&channel=test_channel')
    assert response.status_code == 200
    #Create student
    POST('/students?firstName=test_firstName&lastName=test_lastName&directory_id=test_directory_id&uid=0')
    #Add student to group
    POST('/student/uid/0/group/test_group')

    response = DELETE('/classes?className=test_class')
    assert response.status_code == 204

    #Class was deleted
    assert len(GET('/classes').json()) == 0
    #Group was deleted
    assert len(GET('/groups').json()) == 0
    #Group was removed from student teams
    assert GET('/groups/student/uid/0').status_code == 404
    #Slack Data was deleted
    assert GET('/slackData/group/test_group').status_code == 404
    #ELMS Data was deleted
    assert GET('/elmsData/student/uid/0/class/test_class').status_code == 404
