from django.contrib import admin

# Register your models here.
from apps.category.models import Category


admin.site.register(Category)
