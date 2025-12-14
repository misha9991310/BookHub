import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models

from book_hub.books.models import Genre
from book_hub.common.models import BaseModel


class BaseUserManager(BUM):
    def create_user(self, email, username, is_active=True, is_admin=False, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email.lower()),
            username=username,
            is_active=is_active,
            is_staff=is_admin,
            **extra_fields,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email,
            username=username,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(verbose_name="Биография", default="", blank=True)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/", null=True, blank=True, verbose_name="Аватар")
    favorite_genres = models.ManyToManyField(Genre, related_name="users", blank=True, verbose_name="Любимые жанры")

    objects = BaseUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
