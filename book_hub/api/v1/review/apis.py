from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from book_hub.api.v1.review.serializers import (
    ReviewInputSerializer,
    ReviewOutputSerializer,
    ReviewWithUserWithBookOutputSerializer,
)
from book_hub.reviews.entities import CreateReview
from book_hub.reviews.selectors import ReviewsSelector
from book_hub.reviews.services import ReviewsService


class ReviewCreateApi(APIView):
    @extend_schema(
        summary="Создание отзыва",
        request=ReviewInputSerializer,
        responses=ReviewOutputSerializer,
    )
    def post(self, request: Request) -> Response:
        serializer = ReviewInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review = ReviewsService().review_create(
            owner=request.user,
            create_data=CreateReview(
                book=serializer.validated_data["book"],
                rating=serializer.validated_data["rating"],
                text=serializer.validated_data["text"],
            ),
        )
        output_serializer = ReviewOutputSerializer(review)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ReviewApi(APIView):
    @extend_schema(
        summary="Получение списка всех отзывов для книги",
        responses=ReviewWithUserWithBookOutputSerializer(many=True),
    )
    def get(self, request: Request, book_pk: int) -> Response:
        review = ReviewsSelector.reviews_by_book(book_pk=book_pk)
        serializer = ReviewWithUserWithBookOutputSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
