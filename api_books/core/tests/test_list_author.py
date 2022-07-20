from http import HTTPStatus

import pytest

from api_books.core.models import Author


@pytest.fixture
def create_author(db):
    Author.objects.create(name='Author 1')
    Author.objects.create(name='Author 2')
    Author.objects.create(name='Author 3')
    Author.objects.create(name='Author 4')
    Author.objects.create(name='Author 5')
    Author.objects.create(name='Author 6')


@pytest.fixture
def resp(client, create_author):
    return client.get('/api/authors')


@pytest.fixture
def resp_by_name(client, create_author):
    return client.get('/api/authors?name=Author 1')


def test_list_authors_status_code(resp):

    assert resp.status_code == HTTPStatus.OK


def test_authors_list(resp):

    exp = {
        'list': [
            {'name': 'Author 1'},
            {'name': 'Author 2'},
            {'name': 'Author 3'},
            {'name': 'Author 4'},
            {'name': 'Author 5'},
            {'name': 'Author 6'},
        ]}

    authors_list = resp.json()['list']

    assert len(authors_list) == 6

    assert resp.json() == exp


def test_authors_by_name(resp_by_name):

    exp = {'name': 'Author 1'}

    assert resp_by_name.json() == exp


def test_authors_by_name_not_exist(client, db):

    response_404 = client.get('/api/authors?name=No exist')

    assert response_404.status_code == HTTPStatus.NOT_FOUND
    assert response_404.json() == {'error': 'Author with name No exist not found'}
