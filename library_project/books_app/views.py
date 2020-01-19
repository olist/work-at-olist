from django.shortcuts import render
from rest_framework import views, permissions, status, viewsets, mixins
from django_filters import rest_framework as filters

from books_app.models import Author
from books_app.serializers import AuthorSerializer
from books_app.filters import AuthorFilter

# Create your views here.
class AuthorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuthorFilter
