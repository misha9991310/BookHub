from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from book_hub.books.models import ReadingList
from book_hub.users.models import User


class ReadingListInline(admin.TabularInline):
    model = ReadingList
    extra = 1
    fields = ("book", "list_type", "created_at")
    readonly_fields = ("created_at",)


@admin.register(User)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_superuser", "is_active", "created_at", "updated_at")
    fieldsets = DefaultUserAdmin.fieldsets + (
        (None, {"fields": ("bio", "avatar", "favorite_genres")}),
    )

    list_display = (
        "username",
        "email",
        "is_staff",
        "bio",
        "avatar",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_active",)
    ordering = ("-created_at",)
    inlines = [ReadingListInline]
