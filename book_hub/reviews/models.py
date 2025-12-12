from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from book_hub.books.models import Book
from book_hub.common.models import BaseModel
from book_hub.users.models import User


class Review(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews", verbose_name="Книга")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Пользователь",
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(1, message="Оценка не может быть меньше 1"),
            MaxValueValidator(5, message="Оценка не может быть больше 5"),
        ],
        help_text="Оценка от 1 до 5 звезд",
    )
    text = models.TextField(
        verbose_name="Текст отзыва",
        max_length=2000,
        blank=True,
        null=True,
        help_text="Текст отзыва (необязательно)",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ["book", "user"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв {self.user.username} на {self.book.title} - {self.rating}"


class ReviewLike(BaseModel):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes", verbose_name="Отзыв")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="review_likes",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Лайк отзыва"
        verbose_name_plural = "Лайки отзывов"
        unique_together = ["review", "user"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Лайк {self.user.username} на отзыв {self.review.id}"
