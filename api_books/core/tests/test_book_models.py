from api_books.core.models import Book
from api_books.core.tests.conftest import NUMBER_OF_AUTHORS


def test_book_models(book):
    assert Book.objects.exists()


def test_book_number_of_authors(book):

    assert book.authors.all().count() == NUMBER_OF_AUTHORS


def test_book_authors_name(authors, book):

    # Eu posso confiar na ordem ?

    for expected, got in zip(authors, book.authors.all()):
        assert expected == got


def test_book_str(book):

    assert str(book) == f'{book.name} - {book.publication_year}'


def test_book_to_dict(book):

    expected = {
        'id': book.id,
        'name': book.name,
        'edition': book.edition,
        'publication_year':  book.publication_year,
        'authors': [a.name for a in book.authors.all()]
    }

    assert book.to_dict() == expected
