from django.db.models import QuerySet

from book_hub.users.models import User


class UserSelector:
    @staticmethod
    def user_by_id(user: User) -> QuerySet[User]:
        return User.objects.filter(id=user).select_related("favorite_genres")
