from django.db import models


class Author(models.Model):
    name = models.CharField('Name', max_length=32)
    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    uploaded_at = models.DateTimeField('Updated at', auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['-created_at']


class Book(models.Model):
    name = models.CharField('Name', max_length=32)
    edition = models.CharField('Edition', max_length=32)
    publication_year = models.IntegerField('Publication Year')
    authors = models.ManyToManyField(Author, through='GroupBookAuthor', null=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    uploaded_at = models.DateTimeField('Updated at', auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-created_at']


class GroupBookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT, null=True)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.book)

    class Meta:
        verbose_name = "Group Book Author"
        verbose_name_plural = "Group Book Author s"
