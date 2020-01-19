from django.shortcuts import render
from rest_framework import views, permissions, status, viewsets, mixins
from django_filters import rest_framework as filters

from books_app.models import Author, Book
from books_app.serializers import AuthorSerializer, BookSerializer
from books_app.filters import AuthorFilter, BookFilter

class AuthorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        Viewset to retrieve Author data, only list and retrieve operations allowed.
    """
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuthorFilter

class BookViewSet(viewsets.ModelViewSet):
    """
        Viewset for Book operations, all CRUD operations are available.
    """
    queryset = Book.objects.all().order_by('name')
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter