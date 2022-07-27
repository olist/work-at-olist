from http import HTTPStatus

from django.shortcuts import resolve_url


def test_book_get(client, book):
    resp = client.get(resolve_url('books'))

    expected = [book.to_dict()]

    assert resp.status_code == HTTPStatus.OK
    assert resp.json()['result'] == expected
