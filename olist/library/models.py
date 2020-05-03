from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField('Criado em', auto_now_add=True, null=True)
    uploaded_at = models.DateTimeField('Atualizado em', auto_now=True, null=True)


def __str__(self):
    return self.name


class Meta:
    verbose_name = "Author"
    verbose_name_plural = "Authors"
    ordering = ['-created_at']
