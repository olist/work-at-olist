
from django_filters import rest_framework as filters

from books_app.models import Author, Book

class AuthorFilter(filters.FilterSet):
    """
        FilterSet for Author Viewset
    """
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Author
        fields = ['name',]

class BookFilter(filters.FilterSet):
    """
        FilterSet for Book Viewset
    """
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    publication_year = filters.NumberFilter(field_name='publication_year')
    edition = filters.NumberFilter(field_name='edition')
    author = filters.ModelMultipleChoiceFilter(field_name='authors__id', to_field_name="id",queryset=Author.objects.all())


    class Meta:
        model = Book
        fields = ['name', 'publication_year', 'edition', 'author']