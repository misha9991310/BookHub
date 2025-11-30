from django.urls import path

from book_hub.api.v1.books.apis import (
    BookCreateApi,
    BookDeleteApi,
    BookDetailApi,
    BookListApi,
    BookUpdateApi,
)

urlpatterns = [
    path("", BookListApi.as_view(), name="book-list"),
    path("create/", BookCreateApi.as_view(), name="book-create"), # убрать постфикс
    path("<int:book_pk>/", BookDetailApi.as_view(), name="book-detail"),
    path("<int:book_pk>/update/", BookUpdateApi.as_view(), name="book-update"), # убрать постфикс
    path("<int:book_pk>/delete/", BookDeleteApi.as_view(), name="book-delete"), # убрать постфикс
]
