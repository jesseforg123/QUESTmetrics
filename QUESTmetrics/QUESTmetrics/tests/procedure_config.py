import pytest
from request_maker import GET, PUT, POST, DELETE

@pytest.fixture(autouse=True)
def setup(tmpdir):
    DELETE('/clear')

    yield
