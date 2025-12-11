from django.urls import path
from book_hub.api.v1.users.apis import UserListBookApi


urlpatterns = [
    path("books/", UserListBookApi.as_view(), name="user-book-list"),
    path("register/", UserListBookApi.as_view(), name="user-register"),
    path("profile/", UserListBookApi.as_view(), name="user-profile"),
]
