from django.db import transaction

from book_hub.users.entities import CreateUser
from book_hub.users.models import User


class UserService:
    @transaction.atomic
    def user_create(self, create_data: CreateUser) -> User:
        user = User(
            username=create_data.username,
            email=create_data.email,
            bio=create_data.bio,
            avatar=create_data.avatar,
            favorite_genres=create_data.favorite_genres,
        )
        user.set_password(create_data.password)
        user.save()

        return user
