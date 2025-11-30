from django.db import transaction

from book_hub.books.models import Book, Genre, ReadingList
from book_hub.users.models import User


class BookService:
    @transaction.atomic
    def book_create(self, owner: User, **fields) -> Book:
        genres = fields.pop("genres", [])

        book = Book.objects.create(owner=owner, **fields)

        if genres:
            genre_ids = [int(g) for g in genres]
            genre_objects = Genre.objects.filter(id__in=genre_ids)
            book.genres.set(genre_objects)

        return book

    @transaction.atomic
    def book_update(self, book: Book, **fields) -> Book:
        genres = fields.pop("genres", [])

        for attr, value in fields.items():
            setattr(book, attr, value)
        book.save()

        if genres:
            genre_ids = [int(g) for g in genres]
            genre_objects = Genre.objects.filter(id__in=genre_ids)
            book.genres.set(genre_objects)

        return book

    @transaction.atomic
    def book_delete(self, book: Book):
        book.delete()

    @transaction.atomic
    def reading_list_add(self, user: User, book: Book, list_type: str) -> ReadingList:
        reading_list, created = ReadingList.objects.get_or_create(
            user=user,
            book=book,
            list_type=list_type
        )
        return reading_list
