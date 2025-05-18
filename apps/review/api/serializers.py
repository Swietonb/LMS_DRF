from rest_framework import serializers
from apps.review.models import Review
from apps.books.models import Book


class ReviewSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField(
        min_value=1,
        max_value=5,
        help_text='Rating from 1 to 5'
    )
    content = serializers.CharField(
        min_length=10,
        max_length=500,
        help_text='Content of the review'
    )

    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rating', 'content', 'book', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
