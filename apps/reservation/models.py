from django.db import models
from django.utils import timezone
from apps.books.models import Book
from django.contrib.auth.models import User

class Reservation(models.Model):

    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_OVERDUE = 'overdue'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_OVERDUE, 'Overdue'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    reservation_time = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    due_time = models.DateTimeField()
    return_time = models.DateTimeField()

    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"Reservation of '{self.book.title}' ({self.status})"

    @property
    def is_overdue(self):
        """Check if the reservation is overdue."""
        return (
                self.status == self.STATUS_ACTIVE and
                self.due_time and
                timezone.now() > self.due_time
        )

    def mark_as_returned(self):
        """Mark the reservation as completed and set return time."""
        self.status = self.STATUS_COMPLETED
        self.return_time = timezone.now()
        self.save()

        self.book.availability = True
        self.book.save()
