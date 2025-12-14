from collections.abc import Iterable

from django.db import transaction

from book_hub.books.entities import NOT_SET, CreateBook, UpdateBook
from book_hub.books.models import Book, ReadingList
from book_hub.users.models import User


class BookService:
    @staticmethod
    def _set_genres(book: Book, genres_ids: Iterable[int] | None) -> None:
        if genres_ids:
            book.genres.set(genres_ids)

    @transaction.atomic
    def book_create(self, owner: User, create_data: CreateBook) -> Book:
        book = Book.objects.create(
            owner=owner,
            title=create_data.title,
            author=create_data.author,
            cover_image=create_data.cover_image,
            description=create_data.description,
            year_published=create_data.year_published,
            status=create_data.status,
            isbn=create_data.isbn,
        )

        self._set_genres(book=book, genres_ids=create_data.genres)

        return book

    @transaction.atomic
    def book_update(self, book: Book, update_data: UpdateBook) -> Book:
        update_fields = []

        for field_name in [ # что-нибудь придумать здесь
            "title",
            "author",
            "description",
            "year_published",
            "status",
            "isbn",
            "cover_image",
        ]:
            value = getattr(update_data, field_name, None)
            if value is not NOT_SET:
                setattr(book, field_name, value)
                update_fields.append(field_name)

        if update_data.genres is not NOT_SET:
            self._set_genres(book, update_data.genres)

        if update_fields:
            book.save(update_fields=update_fields)

        return book

    def book_delete(self, book: Book) -> None:
        book.delete()

    def reading_list_add(self, user: User, book: Book, list_type: str) -> ReadingList:
        return ReadingList.objects.get_or_create(user=user, book=book, defaults={"list_type": list_type})[0] # возможно стоит ошибку обработать и вернуть None
