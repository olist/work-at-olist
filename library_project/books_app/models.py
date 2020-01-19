from django.db import models

# Create your models here.
class Author(models.Model):
    """
        Class representing authors of books
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
        Class representing books.
        Books can have many authors, and authors can have many books
    """
    name = models.CharField(max_length=100) 
    publication_year = models.PositiveIntegerField()
    edition = models.PositiveIntegerField()
    authors = models.ManyToManyField(Author, related_name='books')