from django.db.models import QuerySet

from book_hub.users.models import User


class UserSelector:
    @staticmethod
    def user_by_id(user_id: int) -> QuerySet[User]:
        return User.objects.filter(user_id=user_id).select_related("favorite_genres")
