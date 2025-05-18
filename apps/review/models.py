from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.books.models import Book
from django.contrib.auth.models import User


class Review(models.Model):

    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                     MaxValueValidator(5)])
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']  # - descending
        unique_together = ['user', 'book']  # user can add only one review to each book

    def __str__(self):
        return f"Review for {self.book.title} - {self.rating}/5"
