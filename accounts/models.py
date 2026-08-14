from django.contrib.auth.models import AbstractUser
from django.db import models


# ==========================================
# CUSTOM USER
# ==========================================

class User(AbstractUser):

    class Gender(models.TextChoices):

        MALE = "Male", "Male"
        FEMALE = "Female", "Female"
        OTHER = "Other", "Other"
        PREFER_NOT_TO_SAY = "Prefer Not To Say", "Prefer Not To Say"

    email = models.EmailField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        blank=True
    )

    is_email_verified = models.BooleanField(
        default=False
    )

    marketing_emails = models.BooleanField(
        default=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username"
    ]

    def __str__(self):

        return self.email


# ==========================================
# USER ADDRESS
# ==========================================

class Address(models.Model):

    class AddressType(models.TextChoices):

        HOME = "HOME", "Home"
        WORK = "WORK", "Work"
        OTHER = "OTHER", "Other"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses"
    )

    full_name = models.CharField(
        max_length=120
    )

    phone_number = models.CharField(
        max_length=15
    )

    address_line_1 = models.CharField(
        max_length=255
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    postal_code = models.CharField(
        max_length=20
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    address_type = models.CharField(
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.HOME
    )

    is_default = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "-is_default",
            "-created_at"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "is_default"],
                condition=models.Q(is_default=True),
                name="unique_default_address_per_user",
            )
        ]

    def __str__(self):

        return f"{self.full_name} - {self.city}"

# =====================================================
# USER SESSION
# =====================================================

class UserSession(models.Model):
    """
    Stores login sessions for security tracking.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    session_key = models.CharField(
        max_length=64,
        unique=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    browser = models.CharField(
        max_length=150,
        blank=True,
    )

    operating_system = models.CharField(
        max_length=150,
        blank=True,
    )

    device = models.CharField(
        max_length=150,
        blank=True,
    )

    last_activity = models.DateTimeField(
        auto_now=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-last_activity",
        ]

    def __str__(self):

        return (
            f"{self.user.email} - {self.browser}"
        )