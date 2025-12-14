from uuid import UUID

from django.db.models import QuerySet

from book_hub.users.models import User


class UserSelector:
    @staticmethod
    def user_by_id(user_id: UUID) -> QuerySet[User]:
        return User.objects.filter(id=user_id).prefetch_related("favorite_genres")
