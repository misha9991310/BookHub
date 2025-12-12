from django.urls import path

from book_hub.api.v1.review.apis import (
    ReviewApi,
    ReviewCreateApi,
)

urlpatterns = [
    path("", ReviewCreateApi.as_view(), name="review-list"),
    path("<int:book_pk>/", ReviewApi.as_view(), name="review-detail"),
]
