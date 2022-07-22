from django.db import models


class Author(models.Model):
    name = models.CharField('Nome', max_length=120, unique=True)

    def __str__(self):
        return f'Autor: {self.name}'

    def to_dict(self):
        return dict(id=self.id, name=self.name)
