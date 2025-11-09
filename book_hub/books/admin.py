from django.contrib import admin

from book_hub.books.models import Book, Genre, ReadingList


# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'author', 'cover_image', 'description', 'year_published', 'status', 'isbn',]
    search_fields = ['title', 'author', 'genres',]



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug',]
    search_fields = ['title',]


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'type', 'added_date',]
    search_fields = ['user',]
