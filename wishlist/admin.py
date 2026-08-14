from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "user",
        "session_key",
        "created_at",
    )

    search_fields = (
        "product__name",
        "user__username",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )