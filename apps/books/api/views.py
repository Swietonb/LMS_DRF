from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from apps.books.models import Book
from apps.books.api.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer

    @swagger_auto_schema(
        operation_description="Get a list of all available categories"
    )
    def list(self, request, *args, **kwargs):
        """Get a list of all available categories."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new category in the system"
    )
    def create(self, request, *args, **kwargs):
        """Create a new category."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get detailed information about a category"
    )
    def retrieve(self, request, *args, **kwargs):
        """Get details of a specific category."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update information about a category"
    )
    def update(self, request, *args, **kwargs):
        """Update all fields of a category."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update information about a category"
    )
    def partial_update(self, request, *args, **kwargs):
        """Update selected fields of a category."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a category from the system"
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a category."""
        return super().destroy(request, *args, **kwargs)
