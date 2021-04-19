import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_get_bad_group():
    response = GET('/slackData/group/not_a_group')
    assert response.status_code == 404

def test_get_bad_table():
    response = GET('/not_a_table/group/not_a_group')
    assert response.status_code == 404

def test_get_empty():
    #Create class
    POST('/classes?className=test_class')
    #Create group in this class
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    response = GET('/slackData/group/test_group')
    assert response.status_code == 200
    assert response.json() is not None and response.json()['result'] == ""

def test_put_bad_file():
    #Create class
    POST('/classes?className=test_class')
    #Create group in this class
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    #No file
    response = PUT('/slackData/group/test_group')
    assert response.status_code == 400

    response = GET('/slackData/group/test_group')
    assert response.status_code == 200
    assert response.json() is not None and response.json()['result'] == ""

    #Misnamed file
    response = response = PUT('/slackData/group/test_group', file='files/messages.csv', attachment_name='bad_name')
    assert response.status_code == 400

    response = GET('/slackData/group/test_group')
    assert response.status_code == 200
    assert response.json() is not None and response.json()['result'] == ""

def test_put_bad_group():
    response = PUT('/slackData/group/not_a_group')
    assert response.status_code == 404

def test_put_bad_table():
    response = PUT('/not_a_table/group/not_a_group')
    assert response.status_code == 404

def test_put_get_basic():
    #Create class
    POST('/classes?className=test_class')
    #Create group in this class
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    p = '/Users/stschoberg/Desktop/435/questmetrics/QUESTmetrics/tests/files/messages.csv'
    response = POST('/slackData/group/test_group?filePath={}'.format(p))
    assert response.status_code == 200

    response = GET('/slackData/group/test_group')
    assert response.status_code == 200
    assert len(response.json())== 1163

    