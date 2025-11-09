from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from book_hub.books.models import ReadingList
from book_hub.users.models import User


class ReadingListInline(admin.TabularInline):
    model = ReadingList
    extra = 1
    fields = ('book', 'type', 'added_date')
    readonly_fields = ('added_date',)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    model = User
    fieldsets = DefaultUserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'avatar', 'favorite_genres')}),
    )

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'bio', 'avatar']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    # list_filter = (...)
    ordering = ('-created_at',)
    inlines = [ReadingListInline]