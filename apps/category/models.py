from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name: str = 'Category'
        verbose_name_plural: str = 'Categories'

    def __str__(self) -> models.CharField:
        return self.name
