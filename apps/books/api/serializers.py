from rest_framework import serializers
from rest_framework.serializers import CharField, BooleanField, IntegerField

from apps.books.models import Book
from apps.category.models import Category


class BookSerializer(serializers.ModelSerializer):

    title: CharField = CharField(
        min_length=3,
        max_length=200,
        help_text='Book title'
    )
    author: CharField = CharField(
        min_length=3,
        max_length=100,
        help_text='Book author'
    )
    ISBN: CharField = CharField(
        min_length=17,
        max_length=17,
        help_text='ISBN Number with (-)',
        required=False
    )
    description: CharField = CharField(
        min_length=3,
        max_length=500,
        help_text='Book description',
        required=False
    )
    year: IntegerField = IntegerField(
        min_value=1500,
        max_value=2100,
        help_text='Release year'
    )
    availability: BooleanField = BooleanField(
        default=True,
        help_text='Availability status'
    )
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'ISBN', 'description',
                  'year', 'availability', 'categories']
        read_only_fields = ['id']
