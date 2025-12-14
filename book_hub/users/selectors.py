from uuid import UUID

from book_hub.users.models import User


class UserSelector:
    @staticmethod
    def user_by_id(user_id: UUID, prefetch_related_fields: list[str] | None = None) -> User:
        base_qs = User.objects.filter(id=user_id)

        if prefetch_related_fields:
            base_qs.prefetch_related(*prefetch_related_fields)

        return base_qs.first()
