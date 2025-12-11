from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from book_hub.api.v1.books.serializers import (
    BookListOutputSerializer,
    ReadingListOutputSerializer,
)
from book_hub.books.selectors import BookSelector


class UserRegisterApi(APIView):

    @extend_schema(
        summary="Регистрация пользователя",
        responses=BookListOutputSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        books = BookSelector.reading_lists_by_user(
            user=request.user
        )
        serializer = ReadingListOutputSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileApi(APIView):

    @extend_schema(
        summary="Получить профиль пользователя",
        responses=BookListOutputSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        books = BookSelector.reading_lists_by_user(
            user=request.user
        )
        serializer = ReadingListOutputSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Получить профиль пользователя",
        responses=BookListOutputSerializer(many=True),
    )
    def patch(self, request: Request) -> Response:
        books = BookSelector.reading_lists_by_user(
            user=request.user
        )
        serializer = ReadingListOutputSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListBookApi(APIView):

    @extend_schema(
        summary="Получение списка всех книг пользователя",
        responses=BookListOutputSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        books = BookSelector.reading_lists_by_user(
            user=request.user
        )
        serializer = ReadingListOutputSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
