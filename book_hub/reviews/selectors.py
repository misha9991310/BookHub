from django.db.models import QuerySet

from book_hub.reviews.models import Review


class ReviewsSelector:
    def __init__(self, review: Review | None = None) -> None:
        self._review = review

    @classmethod
    def review_list(cls) -> QuerySet[Review]:
        return Review.objects.all()

    @classmethod
    def reviews_by_book(cls, book_pk: int) -> QuerySet[Review]:
        return (
            Review.objects.filter(book_id=book_pk).select_related("user").prefetch_related("likes")
        )

    @classmethod
    def reviews_by_user(cls, user_id: int) -> QuerySet[Review]:
        return Review.objects.filter(user_id=user_id).select_related("book")
