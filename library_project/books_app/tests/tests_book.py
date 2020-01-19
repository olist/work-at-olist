from django.test import TestCase, Client
from rest_framework.test import APIClient

from library_project.settings import REST_FRAMEWORK as drf_configs
from books_app.models import Author, Book
from books_app.serializers import BookSerializer, AuthorSerializer
import json
import collections

# Create your tests here.

class AuthorViewsTest(TestCase):

    client = APIClient()

    AUTHORS = [
        {'name':'Mário de Andrade'},
        {'name':'Clarice Linspector'},
        {'name':'Carlos Drummond de Andrade'},
        {'name':'Guimarães Rosa'},
    ]

    

    def setUp(self):
        """
            Setting up test database
        """
        authors = [Author(name=name) for name in self.AUTHORS]
        Author.objects.bulk_create(authors, ignore_conflicts=True)

        books = [
            {'name': 'Macunaíma', 'publication_year': 1928, 'edition': 1, 'authors': [1]},
            {'name': 'A Hora da Estrela', 'publication_year': 1977, 'edition': 1, 'authors': [2]},
            {'name': 'The Minus Sign', 'publication_year': 1980, 'edition': 1, 'authors': [3]},
            {'name': 'Sagarana', 'publication_year': 1946, 'edition': 2, 'authors': [4]},
            {'name': 'Example Book', 'publication_year': 1980, 'edition': 1, 'authors': [3, 4]},
            {'name': 'Other Example Book', 'publication_year': 1995, 'edition': 1, 'authors': [3, 4]},
        ]
        for book in books:
            book_authors = book.pop('authors')
            book_object = Book.objects.create(**collections.OrderedDict(book))
            book_object.authors.set(book_authors)
            book_object.save()

    def test_list_books_endpoint(self):
        """
            Test GET request in Books endpoint
        """
        response = self.client.get("/books/")
        self.assertEquals(response.status_code, 200)

    def test_get_books(self):
        """
            Teste the GET (list) request content
        """
        response = self.client.get("/books/")
        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEquals(content['count'], Book.objects.all().count())
        self.assertTrue(len(content['results']) <= drf_configs['PAGE_SIZE'] )
        
        self.assertTrue('id' in content['results'][0].keys())
        self.assertTrue('name' in content['results'][0].keys())
        self.assertTrue('publication_year' in content['results'][0].keys())
        self.assertTrue('edition' in content['results'][0].keys())
        self.assertTrue('authors' in content['results'][0].keys())
    
    def test_book_json_content(self):
        """
            Test the content of result content when at least one book is retrieved
        """
        response = self.client.get("/books/")
        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEquals(content['count'], Book.objects.all().count())
        self.assertTrue(len(content['results']) <= drf_configs['PAGE_SIZE'] )
        # test data types of book fields        
        self.assertTrue(isinstance(content['results'][0]['id'], int))
        self.assertTrue(isinstance(content['results'][0]['name'], str))
        self.assertTrue(isinstance(content['results'][0]['publication_year'], int))
        self.assertTrue(isinstance(content['results'][0]['edition'], int))
        self.assertTrue(isinstance(content['results'][0]['authors'], list))
    
    def test_create_book_success(self):
        """
            Test creation of a book, using POST method
        """
        json_ = {
            'name': 'test',
            'publication_year': 2019,
            'edition': 1,
            'authors': [1,3]
        }
        response = self.client.post('/books/', data=json_)
        self.assertEquals(response.status_code, 201)
        content = json.loads(response.content)
        self.assertTrue('id' in content.keys())
        self.assertTrue(content['name'] == json_['name'])
        self.assertTrue(content['publication_year'] == json_['publication_year'])
        self.assertTrue(content['edition'] == json_['edition'])
        self.assertTrue(content['authors'] == json_['authors'])
        self.assertTrue(Book.objects.get(id=content['id']))

    def test_create_book_fail_invalid_name(self):
        """
            Test the response of the endpoint when a blank name is passed
        """
        json_ = {
            'name': '',
            'publication_year': 2019,
            'edition': 1,
            'authors': [1,3]
        }
        response = self.client.post('/books/', data=json_)
        self.assertEquals(response.status_code, 400)
        content = json.loads(response.content)
        self.assertTrue('name' in content.keys())
        self.assertEquals(content['name'], ['This field may not be blank.'])
    
    def test_create_book_fail_invalid_publication_year(self):
        """
            Test the response of the endpoint when negative year is passed
        """
        json_ = {
            'name': 'test',
            'publication_year': -2019,
            'edition': 1,
            'authors': [1,3]
        }
        response = self.client.post('/books/', data=json_)
        self.assertEquals(response.status_code, 400)
        content = json.loads(response.content)
        self.assertTrue('publication_year' in content.keys())
        self.assertEquals(content['publication_year'], ['publication_year must be a positive integer.'])

    def test_create_book_fail_invalid_edition(self):
        """
            Test the response of the endpoint when a negative edition is passed
        """
        json_ = {
            'name': 'test',
            'publication_year': 2019,
            'edition': -1,
            'authors': [1,3]
        }
        response = self.client.post('/books/', data=json_)
        self.assertEquals(response.status_code, 400)
        content = json.loads(response.content)
        self.assertTrue('edition' in content.keys())
        self.assertEquals(content['edition'], ['edition must be a positive integer.'])

    def test_create_book_fail_authors_empty(self):
        """
            Test to not create a book without authors
        """
        json_ = {
            'name': 'test',
            'publication_year': 2019,
            'edition': 1,
            'authors': []
        }
        response = self.client.post('/books/', data=json_)
        self.assertEquals(response.status_code, 400)
        content = json.loads(response.content)
        self.assertTrue('authors' in content.keys())
        self.assertEquals(content['authors'], ['This list may not be empty.'])

    def test_book_serializer_authors__contains_all_data(self):
        """
            Test the content of authors field in book, to be equal do serializer
        """
        response = self.client.get("/books/1/")
        content = json.loads(response.content)
        author = Author.objects.get(id=1)
        author_serializer_data = AuthorSerializer([author], many=True).data
        # check if all author data is being returned
        self.assertEquals(content['authors'], author_serializer_data)

    def test_book_search_by_name(self):
        """
            Test book search using query: name
        """
        response = self.client.get("/books/?name=Example")
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 2)
        queryset = Book.objects.filter(name__icontains="Example")
        ids = list(map(lambda book: book.id, queryset))
        ids_response = list(map(lambda response_object: response_object['id'], content['results']))
        self.assertEquals(sorted(ids), sorted(ids_response))    

    def test_book_search_by_publication_year(self):
        """
            Test book search using query: publication_year
        """
        response = self.client.get("/books/?publication_year=1980")
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 2)
        queryset = Book.objects.filter(publication_year=1980)
        ids = list(map(lambda book: book.id, queryset))
        ids_response = list(map(lambda response_object: response_object['id'], content['results']))
        self.assertEquals(sorted(ids), sorted(ids_response))

    def test_book_search_by_edition(self):
        """
            Test book search using query: edition
        """
        response = self.client.get("/books/?edition=1")
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 5)
        queryset = Book.objects.filter(edition=1)
        ids = list(map(lambda book: book.id, queryset))
        ids_response = list(map(lambda response_object: response_object['id'], content['results']))
        self.assertEquals(sorted(ids), sorted(ids_response))

    def test_book_search_by_authors(self):
        """
            Test book search using author as a parameter
        """
        response = self.client.get("/books/?author=3")
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 3)
        queryset = Book.objects.filter(authors=3)
        ids = list(map(lambda book: book.id, queryset))
        ids_response = list(map(lambda response_object: response_object['id'], content['results']))
        self.assertEquals(sorted(ids), sorted(ids_response))

    def test_combination_edition_author(self):
        """
            Test book search using query combination: author + edition
        """
        response = self.client.get("/books/?author=4&edition=1")
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 2)
        queryset = Book.objects.filter(authors=4, edition=1)
        ids = list(map(lambda book: book.id, queryset))
        ids_response = list(map(lambda response_object: response_object['id'], content['results']))
        self.assertEquals(sorted(ids), sorted(ids_response))

    def test_search_params_empty(self):
        """
            Test book search using query params, but without content
        """
        response = self.client.get("/books/?edition=&publication_year=&name=")
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), Book.objects.all().count())
        queryset = Book.objects.all()
        ids = list(map(lambda book: book.id, queryset))
        ids_response = list(map(lambda response_object: response_object['id'], content['results']))
        self.assertEquals(sorted(ids), sorted(ids_response))

    def test_patch_book(self):
        """
            Test patch request to change one param
        """
        json_ = {"name": "Alternative name"}
        response = self.client.patch("/books/1/", data=json_, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        book = Book.objects.get(id=1)
        self.assertEquals(book.name, json_['name'])

    def test_patch_book_authors(self):
        """
            Test patch request update authors
        """
        json_ = {"authors": [1, 3]}
        response = self.client.patch("/books/1/", data=json_, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        book = Book.objects.get(id=1)
        authors_ids = list(map(lambda book: book.id, book.authors.all()))
        self.assertEquals(sorted(authors_ids), sorted(json_['authors']))
    
    def test_put_book(self):
        """
            Test put book
        """
        json_ = {"name": "TEST", "publication_year": 2000, "edition": 1,"authors": [1, 3]}
        response = self.client.put("/books/1/", data=json_, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        book = Book.objects.get(id=1)
        self.assertEquals(BookSerializer(book).data, content)

    def test_delete_book(self):
        """
            Teste deletion of a book
        """
        response = self.client.delete("/books/1/")
        self.assertEquals(response.status_code, 204)
        
        response_get = self.client.get("/books/1/")
        self.assertEquals(response.status_code, 204)
        content = json.loads(response_get.content)
        self.assertEquals({"detail": "Not found."}, content)