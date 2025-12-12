from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from book_hub.api.v1.users.apis import (
    CustomTokenObtainPairView,
    UserListBookApi,
    UserProfileView,
    UserRegistrationAPI,
)

urlpatterns = [
    path("books/", UserListBookApi.as_view(), name="user-book-list"),
    path("register/", UserRegistrationAPI.as_view(), name="user-register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
