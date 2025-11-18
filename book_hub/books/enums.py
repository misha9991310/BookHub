from django.db import models


class BookStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE"
    READS = "READS"
    IN_ARCHIVE = "IN_ARCHIVE"


class ReadingListType(models.TextChoices):
    WANT_TO_READ = "WANT_TO_READ"
    READING = "READING"
    READ = "READ"
