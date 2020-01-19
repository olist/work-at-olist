from django.shortcuts import render
from rest_framework import views, permissions, status, viewsets, mixins
from django_filters import rest_framework as filters

from books_app.models import Author
from books_app.serializers import AuthorSerializer
from books_app.filters import AuthorFilter

class AuthorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        Viewset to retrieve Author data, only list and retrieve operations allowed.
    """
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuthorFilter

