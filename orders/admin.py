from django.contrib import admin

from .models import Order, OrderItem
from .email_service import (
    send_shipped_email,
    send_delivered_email,
)


# ==========================================
# ORDER ITEMS INLINE
# ==========================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "product",
        "variant",
        "quantity",
        "price",
    )


# ==========================================
# ORDER ADMIN
# ==========================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer_name",
        "payment_status",
        "status",
        "total",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "customer_name",
        "phone",
        "email",
    )

    readonly_fields = (
        "order_number",
        "subtotal",
        "shipping_charge",
        "total",
        "created_at",
        "updated_at",

        # Razorpay
        "razorpay_order_id",
        "razorpay_payment_id",
        "razorpay_signature",
    )

    inlines = [
        OrderItemInline
    ]

    def save_model(self, request, obj, form, change):

        send_shipped = False
        send_delivered = False

        if change:

            old_obj = Order.objects.filter(
                pk=obj.pk
            ).first()

            if old_obj:

                if (
                    old_obj.status != Order.OrderStatus.SHIPPED
                    and obj.status == Order.OrderStatus.SHIPPED
                ):
                    send_shipped = True

                if (
                    old_obj.status != Order.OrderStatus.DELIVERED
                    and obj.status == Order.OrderStatus.DELIVERED
                ):
                    send_delivered = True

        super().save_model(
            request,
            obj,
            form,
            change
        )

        if send_shipped:

            try:

                send_shipped_email(obj)

            except Exception as e:

                print(
                    f"Shipment email failed: {e}"
                )

        if send_delivered:

            try:

                send_delivered_email(obj)

            except Exception as e:

                print(
                    f"Delivery email failed: {e}"
                )


# ==========================================
# ORDER ITEM ADMIN
# ==========================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "variant",
        "quantity",
        "price",
    )

    search_fields = (
        "order__order_number",
        "product__name",
    )