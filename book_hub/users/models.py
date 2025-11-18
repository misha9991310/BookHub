import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from book_hub.books.models import Genre
from book_hub.common.models import BaseModel


class User(BaseModel, AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(verbose_name="Биография")
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d/", null=True, blank=True, verbose_name="Аватар"
    )
    favorite_genres = models.ManyToManyField(
        Genre, related_name="users", blank=True, verbose_name="Любимые жанры"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
