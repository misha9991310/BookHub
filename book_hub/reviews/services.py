from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from book_hub.reviews.entities import CreateReview
from book_hub.reviews.models import Review, ReviewLike
from book_hub.users.models import User


class ReviewsService:
    @transaction.atomic
    def review_create(self, owner: User, create_data: CreateReview) -> Review:
        # обработать integrity error для unique together
        return Review.objects.create(
            book=create_data.book,
            user=owner,
            rating=create_data.rating,
            text=create_data.text,
        )

    @transaction.atomic
    def create_review_like(self, review_pk: int, user_id: UUID) -> ReviewLike:
        try:
            return ReviewLike.objects.create(review_pk=review_pk, user_id=user_id)
        except IntegrityError:
            raise ValidationError("Вы уже лайкали этот отзыв")

    def delete_review_like(self, review_like: ReviewLike) -> None:
        review_like.delete()
