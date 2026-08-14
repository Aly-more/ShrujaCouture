from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Address,
    UserSession,
)


# ==========================================
# USER ADMIN
# ==========================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (

        "email",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "is_staff",
        "is_active",

    )

    list_filter = (

        "is_staff",
        "is_active",
        "is_superuser",

    )

    ordering = (

        "email",

    )

    search_fields = (

        "email",
        "username",
        "first_name",
        "last_name",

    )

    fieldsets = (

        ("Login", {

            "fields": (

                "email",
                "username",
                "password",

            )

        }),

        ("Personal Information", {

            "fields": (

                "first_name",
                "last_name",
                "phone_number",

            )

        }),

        ("Permissions", {

            "fields": (

                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",

            )

        }),

        ("Important Dates", {

            "fields": (

                "last_login",
                "date_joined",

            )

        }),

    )

    add_fieldsets = (

        (

            None,

            {

                "classes": ("wide",),

                "fields": (

                    "email",
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "is_staff",
                    "is_active",

                ),

            },

        ),

    )

# ==========================================
# ADDRESS ADMIN
# ==========================================

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (

        "full_name",
        "user",
        "city",
        "state",
        "address_type",
        "is_default",

    )

    list_filter = (

        "address_type",
        "state",
        "is_default",

    )

    search_fields = (

        "full_name",
        "city",
        "postal_code",
        "phone_number",
        "user__email",

    )

    ordering = (

        "-is_default",
        "-created_at",

    )

# =====================================================
# USER SESSION ADMIN
# =====================================================

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "device",
        "browser",
        "operating_system",
        "ip_address",
        "last_activity",
        "created_at",
    )

    list_filter = (
        "device",
        "browser",
        "operating_system",
        "created_at",
    )

    search_fields = (
        "user__email",
        "ip_address",
        "browser",
        "operating_system",
        "device",
    )

    readonly_fields = (
        "session_key",
        "ip_address",
        "browser",
        "operating_system",
        "device",
        "last_activity",
        "created_at",
    )

    ordering = (
        "-last_activity",
    )