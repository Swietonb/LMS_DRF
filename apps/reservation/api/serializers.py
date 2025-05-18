from rest_framework import serializers
from django.utils import timezone
from apps.reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        user = serializers.StringRelatedField(read_only=True)
        fields = [
            'id', 'status', 'reservation_time', 'due_time', 'user',
            'book', 'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'is_overdue', 'return_time']

    def get_is_overdue(self, obj):
        """Calculate if the reservation is overdue."""
        return obj.is_overdue if hasattr(obj, 'is_overdue') else False

    def validate_due_time(self, value):
        """
        Validate that the due time is in the future.
        """
        if value <= timezone.now():
            raise serializers.ValidationError("Due time must be in the future.")
        return value

    def validate_book(self, value):
        """
        Validate that the book is available for reservation.
        """
        # Skip validation if updating existing reservation
        if self.instance and self.instance.book.id == value.id:
            return value

        if not value.availability:
            raise serializers.ValidationError("This book is not available for reservation.")
        return value

    def validate(self, data):
        """
        Object-level validation to ensure logical consistency.
        """
        # Ensure due_time is after reservation_time
        if 'reservation_time' in data and 'due_time' in data:
            if data['due_time'] <= data['reservation_time']:
                raise serializers.ValidationError({
                    "due_time": "Due time must be after reservation time."
                })

        return data

    def create(self, validated_data):
        """
        Override create method to update book availability.
        """
        # Set the book as unavailable when reserved
        book = validated_data['book']
        if book.availability:
            book.availability = False
            book.save()

        return super().create(validated_data)


class ReservationReturnSerializer(serializers.Serializer):
    """
    Special serializer for handling book returns.
    """
    return_time = serializers.DateTimeField(
        required=False,
        default=timezone.now,
        help_text="When the book was returned (defaults to now)"
    )

    def update(self, instance, validated_data):
        """Handle the return process."""
        instance.status = Reservation.STATUS_COMPLETED
        instance.return_time = validated_data.get('return_time', timezone.now())
        instance.save()

        # Update book availability
        book = instance.book
        book.availability = True
        book.save()

        return instance
