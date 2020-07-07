from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from library.models import Author

mock_authors = [
    {'name': 'Bruce Anstey'},
    {'name': 'John Nelson Darby'},
    {'name': 'Mairo Persona'},
    {'name': 'delete me'}
]


def create_mocks():
    for author in mock_authors:
        Author.objects.create(name=author['name'])


class AuthorViewSetTest(TestCase):
    """
      Test's for Author's endpoint
    """

    def setUp(self):
        self.url = '/api/authors/'
        self.client = APIClient()
        create_mocks()

    def test_create(self):
        res = self.client.post(self.url, {'name': 'Davi'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_with_name(self):
        res = self.client.get(self.url, {'name': 'Bruce Anstey'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['results'][0]['name'], 'Bruce Anstey')

    def test_update(self):
        res = self.client.put(self.url+'3', {'name': 'Mario Persona'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['name'], 'Mario Persona')

    def test_delete(self):
        res = self.client.delete(self.url+'4')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
