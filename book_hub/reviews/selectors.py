from django.db.models import QuerySet

from book_hub.reviews.models import Review


class ReviewsSelector:
    def __init__(self, review: Review | None = None) -> None:
        self._review = review

    @staticmethod
    def review_list() -> QuerySet[Review]:
        return Review.objects.all()

    @staticmethod
    def reviews_by_book(book_pk: int) -> QuerySet[Review]:
        return (
            Review.objects.filter(book_id=book_pk).select_related("user").prefetch_related("likes")
        )

    @staticmethod
    def reviews_by_user(user_id: int) -> QuerySet[Review]:
        return Review.objects.filter(user_id=user_id).select_related("book")
