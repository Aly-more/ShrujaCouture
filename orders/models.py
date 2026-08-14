from django.db import models
from products.models import Product, ProductVariant
from accounts.models import User, Address
from django.core.exceptions import ValidationError


class Order(models.Model):

    class OrderStatus(models.TextChoices):

        PENDING = "Pending", "Pending"
        CONFIRMED = "Confirmed", "Confirmed"
        PACKED = "Packed", "Packed"
        SHIPPED = "Shipped", "Shipped"
        DELIVERED = "Delivered", "Delivered"
        CANCELLED = "Cancelled", "Cancelled"

    class PaymentStatus(models.TextChoices):

        PENDING = "Pending", "Pending"
        PAID = "Paid", "Paid"
        FAILED = "Failed", "Failed"
        REFUNDED = "Refunded", "Refunded"

    order_number = models.CharField(
        max_length=30,
        unique=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    # Snapshot of shipping information
    customer_name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    shipping_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    notes = models.TextField(
        blank=True
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    estimated_delivery = models.DateField(
        null=True,
        blank=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def clean(self):

        if (
            self.payment_status != self.PaymentStatus.PAID
            and self.status in [
                self.OrderStatus.CONFIRMED,
                self.OrderStatus.PACKED,
                self.OrderStatus.SHIPPED,
                self.OrderStatus.DELIVERED,
            ]
        ):

            raise ValidationError(
                "Order cannot be confirmed or processed until payment is completed."
            )


    def save(self, *args, **kwargs):

            self.full_clean()

            super().save(*args, **kwargs)


    def __str__(self):

        return self.order_number


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:

        ordering = [
            "id"
        ]

    def __str__(self):

        return f"{self.product.name} ({self.variant.size})"