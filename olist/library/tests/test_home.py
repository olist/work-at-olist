import pytest


@pytest.fixture
def resp(client):
    return client.get('/')


def test_name_author(resp):
    assert resp.status_code == 200
