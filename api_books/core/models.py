from django.db import models


class Author(models.Model):
    name = models.CharField('Nome', max_length=120, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'Autor: {self.name}'

    def to_dict(self):
        return dict(id=self.id, name=self.name)


class Book(models.Model):
    name = models.CharField('Nome', max_length=120, unique=True)
    edition = models.PositiveSmallIntegerField('Edição')
    publication_year = models.CharField('Edição', max_length=4)
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return f'{self.name} - {self.publication_year}'
