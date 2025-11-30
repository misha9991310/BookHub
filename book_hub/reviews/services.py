from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from book_hub.reviews.models import Review, ReviewLike


class ReviewsService:
    def review_create(self, **fields) -> Review:
        return Review.objects.create(**fields)

    def review_update(self, review: Review, **fields) -> Review:  # добавить dto
        for attr, value in fields.items():  # как сделать апдейт на None 
            setattr(review, attr, value)
        review.save()

        return review

    def create_review_like(self, review_pk: int, user_id: UUID) -> ReviewLike:
        try:
            return ReviewLike.objects.create(review_pk=review_pk, user_id=user_id)
        except IntegrityError:
            raise ValidationError("Вы уже лайкали этот отзыв")

    def delete_review_like(self, review_like: ReviewLike) -> None:
        review_like.delete()
