import pytest
from request_maker import GET, PUT, POST, DELETE
from procedure_config import setup

def test_requiredArgs_checked():
    #Is our assumption that the parser checks required data realistic?
    response = POST('/students?uid=0')
    assert response.status_code == 400

def test_SQLinjection():
    #Can we trust the session to check?
    POST('/classes?className=test_class')
    POST('/groups?name=test_group&className=test_class&channel=test_channel')

    maliciousQuery = "test_group; DELETE FROM GROUPS WHERE name=test_group;"

    response = GET('/group/health/' + maliciousQuery)

    response = GET('/groups')
    assert len(response.json()) == 1