from django.test import TestCase
from library.models import Author


def create_author(name):
    return Author.objects.create(name=name)


class AuthorTest(TestCase):
    """
      Test for Author model
    """
    def test_create(self):
        author = create_author('Paulo de Tarso')
        self.assertEqual(author.name, author.__str__())
