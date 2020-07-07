from rest_framework import  viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import AuthorSerializer
from .models import Author


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    filterset_fields = ('name',)
    paginate_by = '10'
