from django.db.models import Prefetch, QuerySet

from book_hub.books.models import Book, Genre, ReadingList
from book_hub.users.models import User


class BookSelector:
    @staticmethod
    def book_list() -> QuerySet[Book]:
        return Book.objects.all()

    @staticmethod
    def book_detail(book_pk: int) -> Book | None:
        return (
            Book.objects.filter(pk=book_pk)
            .select_related("owner")
            .prefetch_related("genres", "reviews", "reading_lists")
            .first()
        )

    @staticmethod
    def books_by_owner(owner_id: int) -> QuerySet[Book]:
        return Book.objects.filter(owner_id=owner_id).select_related("owner")

    @staticmethod
    def books_by_pk(book_pk: int) -> Book:
        return Book.objects.filter(book=book_pk).first()

    @staticmethod
    def reading_lists_by_user(user: User) -> QuerySet[ReadingList]:
        genres_only = Genre.objects.only("title")
        return (
            ReadingList.objects.filter(user=user)
            .select_related("book", "user")
            .prefetch_related(Prefetch("book__genres", queryset=genres_only, to_attr="genres_only"))
        )

    # .only("user__username", "user__avatar")
