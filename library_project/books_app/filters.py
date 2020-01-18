
from django_filters import rest_framework as filters

from books_app.models import Author

class AuthorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Author
        fields = ['name',]