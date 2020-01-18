from django.shortcuts import render
from rest_framework import views, permissions, status, viewsets, mixins

from books_app.models import Author
from books_app.serializers import AuthorSerializer

# Create your views here.
class AuthorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
