from django.db import models


class Book(models.Model):
    name = models.CharField('Nome', max_length=120)

    def __str__(self):
        return f'Autor: {self.name}'
