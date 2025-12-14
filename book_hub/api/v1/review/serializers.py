from rest_framework import serializers

from book_hub.api.v1.books.serializers import BookListOutputSerializer
from book_hub.api.v1.users.serializers import UserMinimalOutputSerializer
from book_hub.reviews.models import Review, ReviewLike


class ReviewWithUserWithBookOutputSerializer(serializers.ModelSerializer): # ReviewOutputSerializer
    user = UserMinimalOutputSerializer(read_only=True)
    book = BookListOutputSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "book",
            "rating",
            "text",
            "likes_count",
            "has_liked",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_likes_count(self, obj) -> int:
        return ReviewLike.objects.count()

    def get_has_liked(self, obj) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class ReviewInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "book",
            "rating",
            "text",
        ]

    def validate(self, attrs):
        request = self.context.get("request")
        book = attrs.get("book")

        if request and book:
            if Review.objects.filter(book=book, user=request.user).exists():
                raise serializers.ValidationError("Вы уже оставляли отзыв на эту книгу")
        return attrs


class ReviewOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "book",
            "rating",
            "text",
        ]
