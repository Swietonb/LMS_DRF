from django.contrib import admin

# Register your models here.
from apps.books.models import Book


admin.site.register(Book)


# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'year', 'availability')
#     list_filter = ('availability', 'year')
#     search_fields = ('title', 'author', 'ISBN')