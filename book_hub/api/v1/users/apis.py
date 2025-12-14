from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from book_hub.api.permission import IsOwnerOrReadOnly
from book_hub.api.v1.books.serializers import (
    BookListOutputSerializer,
    ReadingListOutputSerializer,
)
from book_hub.api.v1.users.serializers import (
    CustomTokenObtainPairSerializer,
    RegistrationSerializer,
    UserProfileOutputSerializer,
)
from book_hub.books.selectors import BookSelector
from book_hub.users.models import User
from book_hub.users.selectors import UserSelector


class UserRegistrationAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @extend_schema(
        summary="Регистрация пользователя",
        request=RegistrationSerializer,
        responses=UserProfileOutputSerializer,
    )
    def post(self, request: Request) -> Response:
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        refresh = RefreshToken.for_user(user)
        user_serializer = UserProfileOutputSerializer(user)
        return Response(
            {
                "user": user_serializer.data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Выход из аккаунта",
    )
    def post(self, request: Request) -> Response:
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Успешный выход из системы"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Неверный токен"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserListBookApi(APIView):
    serializer_class = ReadingListOutputSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    @extend_schema(
        summary="Получить список чтения пользователя",
        responses=BookListOutputSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        books = BookSelector.reading_lists_by_user(user=request.user)
        serializer = ReadingListOutputSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    serializer_class = UserProfileOutputSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Получить профиль пользователя",
        responses=UserProfileOutputSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        user = UserSelector.user_by_id(user_id=request.user.id)
        serializer = UserProfileOutputSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
