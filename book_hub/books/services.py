from collections.abc import Iterable

from django.db import transaction

from book_hub.books.models import Book, Genre, ReadingList
from book_hub.users.models import User


class BookService:
    @staticmethod
    def _set_genres(book: Book, genres_ids: Iterable[int] | None) -> None:
        if genres_ids:
            genre_ids = [int(g) for g in genres_ids]
            book.genres.set(Genre.objects.filter(id__in=genre_ids))

    @transaction.atomic
    def book_create(self, owner: User, **fields) -> Book:
        genres_ids = fields.pop("genres", [])
        book = Book.objects.create(owner=owner, **fields)

        self._set_genres(book=book, genres_ids=genres_ids)

        return book

    @transaction.atomic
    def book_update(self, book: Book, **fields) -> Book:
        genres = fields.pop("genres", [])

        for attr, value in fields.items():
            setattr(book, attr, value)
        book.save()

        if genres:  # метод использовать
            genre_ids = [int(g) for g in genres]
            genre_objects = Genre.objects.filter(id__in=genre_ids)
            book.genres.set(genre_objects)

        return book

    def book_delete(self, book: Book):
        book.delete()

    def reading_list_add(self, user: User, book: Book, list_type: str) -> ReadingList:
        return ReadingList.objects.get_or_create(
            user=user, book=book, defaults={"list_type": list_type}
        )[0]
