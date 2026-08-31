from django.contrib import admin

from .models import Author, Book, Condition, Copy, Genre, Location, Publisher


@admin.register(Author, Genre, Publisher, Location, Condition)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class CopyInline(admin.TabularInline):
    model = Copy
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'publisher']
    list_filter = ['genres', 'publisher', 'year']
    search_fields = ['title', 'authors__name']
    filter_horizontal = ['authors', 'genres']
    inlines = [CopyInline]


@admin.register(Copy)
class CopyAdmin(admin.ModelAdmin):
    list_display = ['book', 'location', 'condition']
    list_filter = ['location', 'condition']
    search_fields = ['book__title']
