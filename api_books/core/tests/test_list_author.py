from http import HTTPStatus

import pytest

from django.shortcuts import resolve_url

from api_books.core.models import Author


@pytest.fixture
def authors(db):
    Author.objects.bulk_create((Author(name=f'Author {i}') for i in range(1, 7)))
    return Author.objects.all()


def test_authors_list_with_page_and_page_size(client, authors):
    '''
    "previous": "http://testserver/api/authors?page=1&page_size=2"
    '''

    resp = client.get(resolve_url('authors'), {'page': 2, 'page_size': 2})

    data = resp.json()

    exp = [{'id': a.id, 'name': a.name} for a in authors[2:4]]

    assert len(data['result']) == 2
    assert data['result'] == exp
    assert data['count'] == 6
    assert data['current_page'] == 2
    # "previous": "http://testserver/api/authors?page=1&page_size=2"
    assert data['previous'].endswith(f'{resolve_url("authors")}?page=1&page_size=2')
    # "next": "http://testserver/api/authors?page=1&page_size=2"
    assert data['next'].endswith(f'{resolve_url("authors")}?page=3&page_size=2')


def test_authors_list_without_page_size(client, authors):
    '''
    Page size default is 3
    '''

    resp = client.get(resolve_url('authors'), {'page': 2})

    data = resp.json()

    exp = [{'id': a.id, 'name': a.name} for a in authors[3:]]

    assert len(data['result']) == 3
    assert data['result'] == exp
    assert data['count'] == 6
    assert data['current_page'] == 2
    assert data['previous'].endswith(f'{resolve_url("authors")}?page=1&page_size=3')


def test_authors_list_without_page_and_page_size(client, authors):
    '''
    Page size default is 3 and page default 1
    '''

    resp = client.get(resolve_url('authors'))

    data = resp.json()

    exp = [{'id': a.id, 'name': a.name} for a in authors[:3]]

    assert len(data['result']) == 3
    assert data['result'] == exp
    assert data['count'] == 6
    assert data['current_page'] == 1
    assert data['next'].endswith(f'{resolve_url("authors")}?page=2&page_size=3')


def test_authors_by_name(client, authors):

    resp = client.get(resolve_url('authors'), {'name': authors[0].name})

    exp = {'id': authors[0].id, 'name': authors[0].name}

    assert resp.json() == exp


def test_authors_by_name_not_exist(client, db):

    response = client.get(resolve_url('authors'), {'name': 'No exist'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'error': 'Author with name No exist not found'}
