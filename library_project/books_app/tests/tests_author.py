from django.test import TestCase, Client


from library_project.settings import REST_FRAMEWORK as drf_configs
from books_app.models import Author
import json
# Create your tests here.

class AuthorViewsTest(TestCase):

    client = Client()

    AUTHORS = [
        'Mário de Andrade',
        'Clarice Linspector',
        'Carlos Drummond de Andrade',
        'Guimarães Rosa',
        'William Shakespeare',
        'Jorge Amado',
        'Graciliano Ramos',
        'J.K. Rowling',
        'José de Alencar',
        'Cecília Meireles',
        'Monteiro Lobato',
        'Vinicius de Moraes',
        'José Saramago'
    ]

    def setUp(self):
        """
            Setting up test database
        """
        authors = [Author(name=name) for name in self.AUTHORS]
        Author.objects.bulk_create(authors, ignore_conflicts=True)

    def test_list_authors_response_ok(self):
        """
            Test listing all authors endpoint
        """
        response = self.client.get("/authors/")
        self.assertEquals(response.status_code, 200)
    
    def test_list_all_authors_content(self):
        response = self.client.get("/authors/")
        self.assertEquals(response.status_code, 200)
        content = json.loads(content)
        self.assertEquals(content['count'], Author.objects.all().count())
        self.assertEquals(len(content['results']), drf_configs['PAGE_SIZE'])
    
    def test_list_all_authors_content(self):
        response = self.client.get("/authors/")
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(content['count'], Author.objects.all().count())
        self.assertEquals(len(content['results']), drf_configs['PAGE_SIZE'])
    
    def test_list_all_authors_pagination(self):
        response = self.client.get("/authors/?page=1")

        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), drf_configs['PAGE_SIZE'])

    def test_list_all_authors_page_with_less_results(self):
        response = self.client.get("/authors/?page=2")

        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue(len(content['results']) < drf_configs['PAGE_SIZE'])
    
    def test_search_authors_by_exact_name(self):
        response = self.client.get(f"/authors/?name={self.AUTHORS[2]}")
        self.assertEquals(response.status_code, 200)
        # should get only one Author
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 1)

    def test_search_authors_containing_query(self):
        response = self.client.get(f"/authors/?name=José")
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        # should get two authors which names contains the letter 'c'
        self.assertEquals(len(content['results']), 2)

    def test_search_authors_retrieves_nothing(self):
        response = self.client.get(f"/authors/?name=Gustavo")
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 0)
    
    def test_get_author(self):
        response = self.client.get(f"/authors/1/")
        self.assertEquals(response.status_code, 200)
        # should get the first author in thist test database list
        content = json.loads(response.content)
        self.assertEquals(content['name'], self.AUTHORS[0])

    def test_get_author_fails(self):
        response = self.client.get(f"/authors/20/")
        # there is no author with id 10, should fail
        self.assertEquals(response.status_code, 404)
        