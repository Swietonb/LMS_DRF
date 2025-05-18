from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=17, unique=True, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    year = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)
    categories = models.ManyToManyField('category.Category', related_name='books')

    def __str__(self) -> models.CharField:
        return self.title
