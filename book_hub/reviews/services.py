from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from book_hub.reviews.models import Review, ReviewLike


class ReviewsService:
    @transaction.atomic
    def review_create(self, **fields) -> Review:
        review = Review.objects.create(**fields)

        return review

    @transaction.atomic
    def review_update(self, review: Review, **fields) -> Review:
        for attr, value in fields.items():
            setattr(review, attr, value)
        review.save()

        return review

    @transaction.atomic
    def create_review_like(self, review_pk: int, user_id: UUID) -> ReviewLike:
        try:
            like = ReviewLike.objects.create(review_pk=review_pk, user_id=user_id)
            return like

        except IntegrityError:
            raise ValidationError("Вы уже лайкали этот отзыв")

    def delete_review_like(self, review_like: ReviewLike) -> None:
        review_like.delete()
