from django.contrib import admin

from book_hub.books.models import ReadingList
from book_hub.users.models import User


class ReadingListInline(admin.TabularInline):
    model = ReadingList
    extra = 1
    fields = ("book", "list_type", "created_at")
    readonly_fields = ("created_at",)


@admin.register(User)
class BaseUserAdmin(admin.ModelAdmin):
    fields = [
        "username",
        "email",
        "password",
        "bio",
        "avatar",
        "favorite_genres",
    ]

    list_display = ("username", "email", "is_staff", "is_active", "created_at")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("-created_at",)
    inlines = [ReadingListInline]

    add_fields = ["username", "email", "password1", "password2"]
