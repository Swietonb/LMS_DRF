from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from apps.category.models import Category
from apps.category.api.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_description="Get a list of all available books"
    )
    def list(self, request, *args, **kwargs):
        """Get a list of all available books."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new book in the system"
    )
    def create(self, request, *args, **kwargs):
        """Create a new book."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get detailed information about a book"
    )
    def retrieve(self, request, *args, **kwargs):
        """Get details of a specific book."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update information about a book"
    )
    def update(self, request, *args, **kwargs):
        """Update all fields of a book."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update information about a book"
    )
    def partial_update(self, request, *args, **kwargs):
        """Update selected fields of a book."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a book from the system"
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a book."""
        return super().destroy(request, *args, **kwargs)
