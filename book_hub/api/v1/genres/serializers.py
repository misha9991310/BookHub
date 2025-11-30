from rest_framework import serializers

from book_hub.books.models import Book, Genre


class GenreOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            "title",
            "slug",
        ]

