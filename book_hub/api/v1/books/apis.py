from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from book_hub.api.v1.books.serializers import (
    BookDetailOutputSerializer,
    BookInputSerializer,
    BookListOutputSerializer,
    ReadingListInputSerializer,
    ReadingListOutputSerializer,
    UpdateBookInputSerializer,
)
from book_hub.books.entities import NOT_SET, CreateBook, UpdateBook
from book_hub.books.selectors import BookSelector
from book_hub.books.services import BookService


class BookListAndCreateApi(APIView):
    @extend_schema(
        summary="Создание новой книги",
        request=BookInputSerializer,
        responses=BookDetailOutputSerializer,
    )
    def post(self, request: Request) -> Response:
        serializer = BookInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = BookService().book_create(
            owner=request.user,
            create_data=CreateBook(
                title=serializer.validated_data["title"],
                author=serializer.validated_data["author"],
                cover_image=serializer.validated_data["cover_image"],
                description=serializer.validated_data["description"],
                year_published=serializer.validated_data["year_published"],
                genres=serializer.validated_data["genres"],
                status=serializer.validated_data["status"],
                isbn=serializer.validated_data["isbn"],
            ),
        )
        output_serializer = BookDetailOutputSerializer(book)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Получение списка всех книг",
        responses=BookListOutputSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        books = BookSelector.book_list()
        serializer = BookListOutputSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookApi(APIView):
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

    @extend_schema(
        summary="Обновление книги",
        request=BookInputSerializer,
        responses=BookDetailOutputSerializer,
    )
    def patch(self, request: Request, book_pk: int) -> Response:
        book = BookSelector.book_detail(book_pk=book_pk)
        if not book:
            return Response({"detail": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND)

        if book.owner != request.user:  # в пермишн
            return Response(
                {"detail": "Нет прав для редактирования этой книги"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UpdateBookInputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_book = BookService().book_update(
            book=book,
            update_data=UpdateBook(
                title=serializer.validated_data.get("title", NOT_SET),
                author=serializer.validated_data.get("author", NOT_SET),
                cover_image=serializer.validated_data.get("cover_image", NOT_SET),
                description=serializer.validated_data.get("description", NOT_SET),
                year_published=serializer.validated_data.get("year_published", NOT_SET),
                genres=serializer.validated_data.get("genres", NOT_SET),
                status=serializer.validated_data.get("status", NOT_SET),
                isbn=serializer.validated_data.get("isbn", NOT_SET),
            ),
        )
        output_serializer = BookDetailOutputSerializer(updated_book)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="Удаление книги")
    def delete(self, request: Request, book_pk: int) -> Response:
        book = BookSelector.book_detail(book_pk=book_pk)
        if not book:
            return Response({"detail": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND)

        if book.owner != request.user:
            return Response({"detail": "Нет прав для удаления этой книги"}, status=status.HTTP_403_FORBIDDEN)

        BookService().book_delete(book)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReadingListAddBookApi(APIView):
    @extend_schema(
        summary="Добавление книги в список для чтения",
        request=ReadingListInputSerializer,
        responses=ReadingListOutputSerializer,
    )
    def post(
        self,
        request: Request,
    ) -> Response:
        serializer = ReadingListInputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_book = BookService().reading_list_add(
            user=request.user,
            book=serializer.validated_data["book"],
            list_type=serializer.validated_data["list_type"],
        )
        output_serializer = ReadingListOutputSerializer(updated_book)

        return Response(output_serializer.data, status=status.HTTP_200_OK)
