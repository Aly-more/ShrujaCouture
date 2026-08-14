from rest_framework import serializers

from .models import Order, OrderItem


# ==========================================
# PLACE ORDER
# ==========================================

class PlaceOrderSerializer(serializers.Serializer):

    address_id = serializers.IntegerField()

    notes = serializers.CharField(
        required=False,
        allow_blank=True
    )


# ==========================================
# ORDER ITEM
# ==========================================

class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    size = serializers.CharField(
        source="variant.size",
        read_only=True
    )

    color = serializers.CharField(
        source="variant.color",
        read_only=True
    )

    image = serializers.ImageField(
        source="product.main_image",
        read_only=True
    )

    class Meta:

        model = OrderItem

        fields = (
            "id",
            "product_name",
            "image",
            "size",
            "color",
            "quantity",
            "price",
        )


# ==========================================
# ORDER
# ==========================================

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    payment_status = serializers.CharField(
        source="get_payment_status_display",
        read_only=True
    )

    status = serializers.CharField(
        source="get_status_display",
        read_only=True
    )

    class Meta:

        model = Order

        fields = (
            "id",
            "order_number",
            "customer_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "pincode",
            "subtotal",
            "shipping_charge",
            "total",
            "payment_status",
            "status",
            "created_at",
            "items",
        )