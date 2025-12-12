from dataclasses import dataclass
from typing import Any

from django.db import models
from django.db.models.fields.files import ImageFieldFile


class BookStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE"
    READS = "READS"
    IN_ARCHIVE = "IN_ARCHIVE"


class ReadingListType(models.TextChoices):
    WANT_TO_READ = "WANT_TO_READ"
    READING = "READING"
    READ = "READ"


NOT_SET = object()


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateBook:
    title: str
    author: str
    cover_image: ImageFieldFile | str | None
    description: str | None
    year_published: int | None
    genres: list[int]
    status: str
    isbn: str | None


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateBook:
    title: Any = NOT_SET
    author: Any = NOT_SET
    cover_image: Any = NOT_SET
    description: Any = NOT_SET
    year_published: Any = NOT_SET
    genres: Any = NOT_SET
    status: Any = NOT_SET
    isbn: Any = NOT_SET
