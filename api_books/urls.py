from django.contrib import admin
from django.urls import path

from api_books.core.views import authors, books

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authors', authors, name='authors'),
    path('api/books', books, name='books')
]