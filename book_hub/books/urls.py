from django.urls import path

from book_hub.api.v1.books.apis import (
    BookApi,
    BookListAndCreateApi,
    ReadingListAddBookApi,
)

urlpatterns = [
    path("", BookListAndCreateApi.as_view(), name="book-list-create"),
    path("<int:book_pk>/", BookApi.as_view(), name="book-detail"),
    path("reading_list/", ReadingListAddBookApi.as_view(), name="book-detail"),
]
