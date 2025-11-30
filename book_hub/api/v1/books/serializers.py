from rest_framework import serializers
from book_hub.books.models import Book, ReadingList, Genre
from book_hub.api.v1.genres.serializers import GenreOutputSerializer
from book_hub.api.v1.users.serializers import UserMinimalOutputSerializer


class BookListOutputSerializer(serializers.ModelSerializer):
    genres = GenreOutputSerializer(many=True, read_only=True)

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
            "slug"
        ]
        read_only_fields = fields


class BookDetailOutputSerializer(serializers.ModelSerializer):
    genres = GenreOutputSerializer(many=True, read_only=True)
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
    genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        required=False
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