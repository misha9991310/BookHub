from django.db.models import QuerySet

from book_hub.books.models import Book, ReadingList


class BookSelector:
    # def __init__(self, book: Book | None = None) -> None:
    #     self.book = book

    @staticmethod
    def book_list() -> QuerySet[Book]:
        return Book.objects.all()

    @staticmethod
    def book_detail(cls, book_pk: int) -> Book | None:
        return (
            Book.objects.filter(pk=book_pk)
            .select_related("owner")
            .prefetch_related("genres", "reviews", "reading_lists")
            .first()
        )

    @staticmethod
    def books_by_owner(cls, owner_id: int) -> QuerySet[Book]:
        return Book.objects.filter(owner_id=owner_id).select_related("owner")

    @staticmethod
    def reading_lists_by_user(cls, user_id: int) -> QuerySet[ReadingList]:
        return (
            ReadingList.objects.filter(user_id=user_id)
            .select_related("book", "user")
            .prefetch_related("book__genres")
        )  # можно добавить only
