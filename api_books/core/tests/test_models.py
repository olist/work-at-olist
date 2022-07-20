import pytest

from api_books.core.models import Book


@pytest.fixture
def create_book(db):
    return Book.objects.create(name='Luciano Ramalho')


def test_models_books(create_book):
    assert Book.objects.exists()


def test_str(create_book):
    assert str(create_book) == f'Autor: {create_book.name}'
