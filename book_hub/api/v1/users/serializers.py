from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from book_hub.books.models import Genre
from book_hub.users.models import User


class GenreOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("title",)


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    # валидация для пароля (буквы+цифры+спец символ)

    class Meta:
        model = User
        fields = ("username", "email", "password")


class UserProfileOutputSerializer(serializers.ModelSerializer):
    favorite_genres = GenreOutputSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "bio",
            "avatar",
            "favorite_genres",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "email", "created_at", "updated_at")


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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserProfileOutputSerializer(self.user)
        data["user"] = serializer.data

        return data
