import pytest

from api_books.core.models import Author


@pytest.fixture
def create_author(db):
    return Author.objects.create(name='Luciano Ramalho')


def test_models_authors(create_author):
    assert Author.objects.exists()


def test_str(create_author):
    assert str(create_author) == f'Autor: {create_author.name}'
