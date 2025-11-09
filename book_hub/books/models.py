from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from book_hub.common.models import BaseModel


class BookStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE"
    READS = "READS"
    IN_ARCHIVE = "IN_ARCHIVE"


class ReadingListType(models.TextChoices):
    WANT_TO_READ = "WANT_TO_READ"
    READING = "READING"
    READ = "READ"



class Genre(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse('genre_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Book(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='books', verbose_name="Владелец")
    author = models.CharField(max_length=200, verbose_name="Автор")
    cover_image = models.ImageField(upload_to='cover_image/%Y/%m/%d/', null=True, blank=True, verbose_name="Изображение обложки")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    year_published = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Год издания")
    slug = models.SlugField(max_length=200, unique=True)
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", related_name='books')
    status = models.CharField(
        max_length=64,  # max([len(value) for value in BookStatus.values])
        choices=BookStatus.choices,
        default=BookStatus.AVAILABLE,
        verbose_name="Статус книги"
    )
    isbn = models.CharField(null=True, blank=True, verbose_name='ISBN', max_length=13, # min_length
                            help_text='13-digit ISBN number', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class ReadingList(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reading_lists',
        verbose_name='Пользователь'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reading_lists',
        verbose_name='Книга'
    )
    type = models.CharField( # list_type
        max_length=20,  # max([len(value) for value in ReadingListType.values])
        choices=ReadingListType.choices,
        verbose_name='Тип списка',
    )
    added_date = models.DateTimeField('Дата добавления', auto_now_add=True)  # created_at из basemodel 

    class Meta:
        verbose_name = 'Список чтения'
        verbose_name_plural = 'Списки чтения'
        unique_together = ['user', 'book', 'type']
        ordering = ['-added_date']

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def clean(self):
        if ReadingList.objects.filter(  #  unique_together достаточно
            user=self.user,
            book=self.book,
            type=self.type
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f'Книга "{self.book.title}" уже находится в списке "{self.type}"'
            )
