from django.db import models

# Create your models here.
class Author(models.Model):
    """
        Class representing authors of books
    """
    name = models.CharField(max_length=50, unique=True)