
import pytest
from api_books.core.management.commands.import_csv import Command
from api_books.core.models import Author


CSV_FILE = 'name\nautor1\n autor2 \nautor3 \nautor4'


@pytest.fixture
def cmd():
    return Command()


def mock_csv_reader(csvfile, delimiter=','):

    list_of_list = [[line] for line in CSV_FILE.split()]

    for c in list_of_list:
        yield c


def test_clean_name_strip(cmd):
    assert cmd._clean_name(' teste ') == 'teste'


def test_import_csv_number(mocker, cmd, db):

    csv_mocker = mocker.patch('api_books.core.management.commands.import_csv.csv')
    mocker.patch('api_books.core.management.commands.import_csv.open')

    csv_mocker.reader = mock_csv_reader

    cmd.handle(file_name='')
    assert Author.objects.count() == 4


def test_import_csv_names(mocker, cmd, db):

    csv_mocker = mocker.patch('api_books.core.management.commands.import_csv.csv')
    mocker.patch('api_books.core.management.commands.import_csv.open')

    csv_mocker.reader = mock_csv_reader

    cmd.handle(file_name='')

    for autor, exp in zip(Author.objects.all(), CSV_FILE.split()[1:]):
        assert autor.name == exp
