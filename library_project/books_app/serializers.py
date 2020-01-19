from rest_framework import serializers
from books_app.models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'name'
        ]

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'name',
            'publication_year',
            'edition',
            'authors'
        ]

    def validate(self, data):

        if data.get("publication_year") <= 0:
            raise serializers.ValidationError({'publication_year': ["publication_year must be a positive integer."]})

        if data.get("edition") <= 0:
            raise serializers.ValidationError({'edition': ["edition must be a positive integer."]})

        return data