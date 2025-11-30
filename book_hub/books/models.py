from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from book_hub.books.enums import BookStatus, ReadingListType
from book_hub.common.models import BaseModel


class Genre(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse("genre_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Book(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="books",
        verbose_name="Владелец",
    )
    author = models.CharField(max_length=200, verbose_name="Автор")
    cover_image = models.ImageField(
        upload_to="cover_image/%Y/%m/%d/",
        null=True,
        blank=True,
        verbose_name="Изображение обложки",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    year_published = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Год издания"
    )
    slug = models.SlugField(max_length=200, unique=True)
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", related_name="books")
    status = models.CharField(
        max_length=max([len(value) for value in BookStatus.values]),
        choices=BookStatus.choices,
        default=BookStatus.AVAILABLE,
        verbose_name="Статус книги",
    )
    isbn = models.CharField(
        null=True,
        blank=True,
        verbose_name="ISBN",
        max_length=13,
        help_text="13-digit ISBN number",
        unique=True,
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class ReadingList(BaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reading_lists",
        verbose_name="Пользователь",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reading_lists",
        verbose_name="Книга",
    )
    list_type = models.CharField(
        max_length=max([len(value) for value in ReadingListType.values]),
        choices=ReadingListType.choices,
        verbose_name="Тип списка",
    )

    class Meta:
        verbose_name = "Список чтения"
        verbose_name_plural = "Списки чтения"
        unique_together = ["user", "book", "list_type"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
