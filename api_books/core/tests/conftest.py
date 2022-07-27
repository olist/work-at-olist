import pytest
from api_books.core.models import Author, Book


@pytest.fixture
def create_author(db):
    return Author.objects.create(name='Luciano Ramalho')


NUMBER_OF_AUTHORS = 5


@pytest.fixture
def authors(db):
    Author.objects.bulk_create((Author(name=f'Author {n}') for n in range(NUMBER_OF_AUTHORS)))
    return Author.objects.all()


@pytest.fixture
def book(authors):
    book = Book.objects.create(name='Book 1', edition=1, publication_year='2000')
    book.authors.set(authors)
    return book
