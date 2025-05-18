from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from apps.review.models import Review
from apps.review.api.serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        operation_description="Get a list of all available reviews"
    )
    def list(self, request, *args, **kwargs):
        """Get a list of all available reviews."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new review in the system"
    )
    def create(self, request, *args, **kwargs):
        """Create a new review."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get detailed information about a review"
    )
    def retrieve(self, request, *args, **kwargs):
        """Get details of a specific review."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update information about a review"
    )
    def update(self, request, *args, **kwargs):
        """Update all fields of a review."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update information about a review"
    )
    def partial_update(self, request, *args, **kwargs):
        """Update selected fields of a review."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a review from the system"
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a review."""
        return super().destroy(request, *args, **kwargs)
