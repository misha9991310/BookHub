from django.urls import path, include

urlpatterns = [
    path("users/", include(("book_hub.users.urls", "users"))),
    path("books/", include(("book_hub.books.urls", "books"))),
    path("reviews/", include(("book_hub.reviews.urls", "reviews"))),
]