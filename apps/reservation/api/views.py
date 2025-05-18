from django.utils import timezone
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.reservation.models import Reservation
from apps.reservation.api.serializers import ReservationSerializer, ReservationReturnSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Optimize query performance with select_related
    queryset = Reservation.objects.select_related('book').all()

    def get_queryset(self):
        """
        Customize queryset based on request parameters.
        Allows filtering for overdue reservations and by user.
        """
        queryset = super().get_queryset()

        # Filter by current user (when user system is implemented)
        # queryset = queryset.filter(user=self.request.user)

        # Filter by overdue status if requested
        overdue = self.request.query_params.get('overdue')
        if overdue and overdue.lower() == 'true':
            queryset = queryset.filter(
                status=Reservation.STATUS_ACTIVE,
                due_time__lt=timezone.now()
            )

        return queryset

    def perform_create(self, serializer):
        """
        Set additional fields when creating a reservation.
        """
        # Will associate current user when user system is implemented
        # serializer.save(user=self.request.user)
        serializer.save()

    @swagger_auto_schema(
        method='post',
        request_body=ReservationReturnSerializer,
        responses={
            status.HTTP_200_OK: ReservationSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request if reservation is already completed"
        },
        operation_description="Return a book and mark the reservation as completed."
    )
    @action(detail=True, methods=['post'], serializer_class=ReservationReturnSerializer)
    def return_book(self, request):
        """
        Special action to handle book returns.
        Updates reservation status and makes the book available again.
        """
        reservation = self.get_object()

        # Check if the book is already returned
        if reservation.status == Reservation.STATUS_COMPLETED:
            return Response(
                {"detail": "This book has already been returned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Process the return
        serializer = ReservationReturnSerializer(
            reservation,
            data=request.data or {}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return updated reservation data
        return Response(ReservationSerializer(reservation).data)

    @swagger_auto_schema(
        operation_description="Get a list of all reservations"
    )
    def list(self, request, *args, **kwargs):
        """Get a list of all reservations."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new reservation"
    )
    def create(self, request, *args, **kwargs):
        """Create a new reservation."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get detailed information about a reservation"
    )
    def retrieve(self, request, *args, **kwargs):
        """Get details of a specific reservation."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a reservation"
    )
    def update(self, request, *args, **kwargs):
        """Update all fields of a reservation."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a reservation"
    )
    def partial_update(self, request, *args, **kwargs):
        """Update selected fields of a reservation."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a reservation"
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a reservation."""
        return super().destroy(request, *args, **kwargs)
