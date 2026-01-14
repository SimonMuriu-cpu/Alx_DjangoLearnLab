from django.contrib import admin

# Register your models here.
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Required: Display title, author, and publication_year
    list_display = ('title', 'author', 'publication_year')
    
    # Required: Add list filters
    list_filter = ('author', 'publication_year')
    
    # Required: Add search capabilities
    search_fields = ('title', 'author')