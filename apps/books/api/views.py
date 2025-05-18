from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from apps.books.models import Book
from apps.category.models import Category
from apps.books.api.serializers import BookSerializer
from apps.books.api.permissions import IsAdminOrReadOnly
from apps.books.api.filters import BookFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = BookFilter

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['title', 'author', 'description', 'ISBN']
    ordering_fields = ['title', 'author', 'year']
    ordering = ['title']

    @swagger_auto_schema(
        operation_description="Get a list of books with pagination and filtering",
        manual_parameters=[
            openapi.Parameter(
                'available', openapi.IN_QUERY,
                description="Filter by availability",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'category_id', openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'author', openapi.IN_QUERY,
                description="Filter by author name (contains)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'title', openapi.IN_QUERY,
                description="Filter by title (contains)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'year', openapi.IN_QUERY,
                description="Filter by publication year",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get a list of all available categories."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new book (admin only)"
    )
    def create(self, request, *args, **kwargs):
        """Create a new book (admin only)."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get detailed information about a specific book"
    )
    def retrieve(self, request, *args, **kwargs):
        """Get details of a specific book."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update all book information (admin only)"
    )
    def update(self, request, *args, **kwargs):
        """Update all fields of a book (admin only)."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update book information (admin only)"
    )
    def partial_update(self, request, *args, **kwargs):
        """Update selected fields of a book (admin only)."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a book from the system (admin only)"
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a book (admin only)."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get all available books",
        responses={200: BookSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all books that are available for reservation."""
        books = self.queryset.filter(availability=True)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get books by specific category",
        responses={200: BookSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='category/(?P<category_id>\d+)')
    def by_category(self, request, category_id):
        """Get all books in a specific category."""
        books = self.queryset.filter(categories__id=category_id)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get books by author name",
        responses={200: BookSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='author/(?P<author_name>[\w\s]+)')
    def by_author(self, request, author_name):
        """Get all books by a specific author."""
        books = self.queryset.filter(author__icontains=author_name)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get books by title",
        responses={200: BookSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='title/(?P<title>[\w\s]+)')
    def by_title(self, request, title):
        """Get all books with a specific title."""
        books = self.queryset.filter(title__icontains=title)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get books by publication year",
        responses={200: BookSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='year/(?P<year>\d+)')
    def by_year(self, request, year):
        """Get all books published in a specific year."""
        books = self.queryset.filter(year=year)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Add a category to a book (admin only)",
        responses={201: "Category added successfully", 400: "Invalid request or category not found"}
    )
    @action(detail=True, methods=['post'], url_path='categories/(?P<category_name>[\w\s]+)')
    def add_category(self, request, pk, category_name):
        """Add a category to a book (admin only)."""
        book = self.get_object()
        try:
            category = Category.objects.get(name=category_name)
            book.categories.add(category)
            return Response({"detail": f"Category '{category_name}' added to book"}, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({"detail": f"Category '{category_name}' not found"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Remove a category from a book (admin only)",
        responses={204: "Category removed successfully", 400: "Invalid request or category not found"}
    )
    @action(detail=True, methods=['delete'], url_path='categories/(?P<category_name>[\w\s]+)')
    def remove_category(self, request, pk, category_name):
        """Remove a category from a book (admin only)."""
        book = self.get_object()
        try:
            category = Category.objects.get(name=category_name)
            if category in book.categories.all():
                book.categories.remove(category)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": f"Book doesn't have category '{category_name}'"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"detail": f"Category '{category_name}' not found"}, status=status.HTTP_400_BAD_REQUEST)
