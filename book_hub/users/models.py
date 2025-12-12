import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from book_hub.books.models import Genre
from book_hub.common.models import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    bio = models.TextField(verbose_name="Биография")
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d/", null=True, blank=True, verbose_name="Аватар"
    )
    favorite_genres = models.ManyToManyField(
        Genre, related_name="users", blank=True, verbose_name="Любимые жанры"
    )

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
