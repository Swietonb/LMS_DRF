from django_filters import rest_framework as filters
from apps.books.models import Book


class BookFilter(filters.FilterSet):
    year_min = filters.NumberFilter(field_name="year", lookup_expr='gte')
    year_max = filters.NumberFilter(field_name="year", lookup_expr='lte')

    class Meta:
        model = Book
        fields = {
            'author': ['exact', 'icontains'],
            'title': ['exact', 'icontains'],
            'year': ['exact'],
            'availability': ['exact'],
            'categories__id': ['exact'],
            'categories__name': ['exact', 'icontains'],
        }
