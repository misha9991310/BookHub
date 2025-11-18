from django.contrib import admin

from book_hub.reviews.models import Review, ReviewLike


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "user",
        "rating",
        "text",
    )
    search_fields = (
        "book",
        "user",
        "rating",
        "text",
    )
    ordering = ("-created_at",)


@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = (
        "review",
        "user",
    )
    search_fields = (
        "review",
        "user",
    )
    ordering = ("-created_at",)
