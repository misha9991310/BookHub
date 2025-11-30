from django.urls import path
from book_hub.api.v1.books.apis import BookListApi, BookCreateApi, BookDetailApi, BookUpdateApi, BookDeleteApi

urlpatterns = [
    path('', BookListApi.as_view(), name='book-list'),
    path('create/', BookCreateApi.as_view(), name='book-create'),
    path('<int:book_pk>/', BookDetailApi.as_view(), name='book-detail'),
    path('<int:book_pk>/update/', BookUpdateApi.as_view(), name='book-update'),
    path('<int:book_pk>/delete/', BookDeleteApi.as_view(), name='book-delete'),
]
