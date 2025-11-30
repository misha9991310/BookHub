from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from book_hub.api.v1.books.serializers import (
    BookDetailOutputSerializer,
    BookInputSerializer,
    BookListOutputSerializer,
)
from book_hub.books.selectors import BookSelector
from book_hub.books.services import BookService


class BookListApi(APIView):
    @extend_schema(
        summary="Получение списка всех книг",
        responses=BookListOutputSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        books = BookSelector.book_list()
        serializer = BookListOutputSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookDetailApi(APIView):
    @extend_schema(
        summary="Получение полной информации книги",
        responses=BookDetailOutputSerializer,
    )
    def get(self, request: Request, book_pk: int) -> Response:
        book = BookSelector.book_detail(book_pk=book_pk)
        if not book:
            return Response({"detail": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookDetailOutputSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookCreateApi(APIView):
    @extend_schema(
        summary="Создание новой книги",
        request=BookInputSerializer,
        responses=BookDetailOutputSerializer,
    )
    def post(self, request: Request) -> Response:
        serializer = BookInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_data = serializer.validated_data
        book_data["owner"] = request.user

        book = BookService().book_create(**book_data) # dto
        output_serializer = BookDetailOutputSerializer(book)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class BookUpdateApi(APIView):
    @extend_schema(
        summary="Обновление книги",
        request=BookInputSerializer,
        responses=BookDetailOutputSerializer,
    )
    def put(self, request: Request, book_pk: int) -> Response:  # реализовать patch
        book = BookSelector.book_detail(book_pk=book_pk)
        if not book:
            return Response({"detail": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND)

        if book.owner != request.user: # в пермишн
            return Response(
                {"detail": "Нет прав для редактирования этой книги"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = BookInputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_book = BookService().book_update(book, **serializer.validated_data)
        output_serializer = BookDetailOutputSerializer(updated_book)

        return Response(output_serializer.data, status=status.HTTP_200_OK)


class BookDeleteApi(APIView):
    @extend_schema(summary="Удаление книги")
    def delete(self, request: Request, book_pk: int) -> Response:
        book = BookSelector.book_detail(book_pk=book_pk)
        if not book:
            return Response({"detail": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND)

        if book.owner != request.user:
            return Response(
                {"detail": "Нет прав для удаления этой книги"}, status=status.HTTP_403_FORBIDDEN
            )

        BookService().book_delete(book)
        return Response(status=status.HTTP_204_NO_CONTENT)
