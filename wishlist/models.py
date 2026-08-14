from django.db import models
from django.conf import settings
from products.models import Product


class Wishlist(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
        null=True,
        blank=True,
    )

    session_key = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = ["-created_at"]

    constraints = [

        models.UniqueConstraint(
            fields=["user", "product"],
            condition=models.Q(user__isnull=False),
            name="unique_user_wishlist",
        ),

        models.UniqueConstraint(
            fields=["session_key", "product"],
            condition=models.Q(session_key__isnull=False),
            name="unique_guest_wishlist",
        ),

    ]

    def __str__(self):

        if self.user:
            return f"{self.user} - {self.product.name}"

        return f"Guest - {self.product.name}"