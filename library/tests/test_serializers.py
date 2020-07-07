from django.test import TestCase
from library.models import Author
from library.serializers import AuthorSerializer


def create_author(name):
    return Author.objects.create(name=name)


class AuthorSerializerTest(TestCase):
    """
      Test's for Author's serializing
    """
    def setUp(self):
        self.serializer_data = {
            'name': 'Salomao'
        }

        author = Author.objects.create(**self.serializer_data)
        self.serializer = AuthorSerializer(instance=author)

    def test_contains_field(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name']))

    def test_content(self):
        expected = {
            'name': 'Salomao'
        }
        self.assertEqual(self.serializer_data, expected)
