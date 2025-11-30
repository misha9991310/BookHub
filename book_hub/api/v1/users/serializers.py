from rest_framework import serializers

from book_hub.books.models import Genre
from book_hub.users.models import User


class GenreOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "title",
        )



class UserMinimalOutputSerializer(serializers.ModelSerializer):
    favorite_genres = GenreOutputSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "avatar",
            "favorite_genres",
        ]
        read_only_fields = fields


class UserDetailOutputSerializer(serializers.ModelSerializer):
    favorite_genres = GenreOutputSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "avatar",
            "favorite_genres",
            "date_joined",
            "created_at",
        ]
        read_only_fields = fields
