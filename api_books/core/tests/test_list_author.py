from http import HTTPStatus

import pytest

from django.shortcuts import resolve_url

from api_books.core.models import Author


@pytest.fixture
def authors(db):
    Author.objects.bulk_create((Author(name=f'Author {i}') for i in range(1, 7)))
    return Author.objects.all()


def test_authors_list(client, authors):

    resp = client.get(resolve_url('authors'))

    exp = {'list': [{'id': a.id, 'name': a.name} for a in authors]}

    authors_list = resp.json()['list']

    assert len(authors_list) == 6

    assert resp.json() == exp


def test_authors_by_name(client, authors):

    resp = client.get(resolve_url('authors'), {'name': authors[0].name})

    exp = {'id': authors[0].id, 'name': authors[0].name}

    assert resp.json() == exp


def test_authors_by_name_not_exist(client, db):

    response = client.get(resolve_url('authors'), {'name': 'No exist'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'error': 'Author with name No exist not found'}
