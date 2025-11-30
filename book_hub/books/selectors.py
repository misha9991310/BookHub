from uuid import UUID

from django.db.models import QuerySet

from book_hub.books.models import Book, ReadingList


class BookSelector:
    def __init__(self, book: Book | None = None) -> None:
        self.book = book

    @classmethod
    def book_list(cls) -> QuerySet[Book]:
        return Book.objects.all()

    @classmethod
    def book_detail(cls, book_pk: int) -> Book | None:
        return Book.objects.filter(pk=book_pk).select_related(
            'owner'
        ).prefetch_related(
            'genres',
            'reviews',
            'reading_lists'
        ).first()

    @classmethod
    def books_by_owner(cls, owner_id: int) -> QuerySet[Book]:
        return Book.objects.filter(owner_id=owner_id).select_related('owner')

    @classmethod
    def reading_lists_by_user(cls, user_id: int) -> QuerySet[ReadingList]:
        return ReadingList.objects.filter(user_id=user_id).select_related(
            'book', 'user'
        ).prefetch_related('book__genres')