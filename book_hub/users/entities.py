from dataclasses import dataclass

from django.db.models.fields.files import ImageFieldFile


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateUser:
    username: str
    email: str
    bio: str
    avatar: ImageFieldFile | None
    favorite_genres: list[int]
    password: str
