from rest_framework import serializers
from apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        min_length=3,
        max_length=50,
        help_text='Category name'
    )

    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']
