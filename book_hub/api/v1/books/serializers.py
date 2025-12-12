from rest_framework import serializers

from book_hub.api.v1.users.serializers import UserMinimalOutputSerializer
from book_hub.books.models import Book, Genre, ReadingList


class GenreOutputForBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            "title",
            "slug",
        ]


class BookListOutputSerializer(serializers.ModelSerializer):
    genres = GenreOutputForBookSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "cover_image",
            "year_published",
            "genres",
            "status",
            "slug",
        ]
        read_only_fields = fields


class BookDetailOutputSerializer(serializers.ModelSerializer):
    genres = GenreOutputForBookSerializer(many=True, read_only=True)
    owner = UserMinimalOutputSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "owner",
            "author",
            "cover_image",
            "description",
            "year_published",
            "genres",
            "status",
            "isbn",
            "slug",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class BookInputSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all(), required=False)

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "cover_image",
            "description",
            "year_published",
            "genres",
            "status",
            "isbn",
        ]


class ReadingListOutputSerializer(serializers.ModelSerializer):
    book = BookListOutputSerializer(read_only=True)
    user = UserMinimalOutputSerializer(read_only=True)

    class Meta:
        model = ReadingList
        fields = [
            "id",
            "user",
            "book",
            "list_type",
            "created_at",
        ]
        read_only_fields = fields


class ReadingListInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = [
            "book",
            "list_type",
        ]


class UpdateBookInputSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "cover_image",
            "description",
            "year_published",
            "genres",
            "status",
            "isbn",
        ]
        extra_kwargs = {
            "title": {"required": False},
            "author": {"required": False},
            "cover_image": {"required": False},
            "description": {"required": False},
            "year_published": {"required": False},
            "status": {"required": False},
            "isbn": {"required": False},
        }
