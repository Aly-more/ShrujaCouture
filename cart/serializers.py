from rest_framework import serializers


# ==========================================
# CART ITEM
# ==========================================

class CartItemSerializer(serializers.Serializer):

    item_key = serializers.CharField()

    product_id = serializers.IntegerField()

    variant_id = serializers.IntegerField()

    slug = serializers.CharField()

    name = serializers.CharField()

    price = serializers.FloatField()

    image = serializers.CharField()

    size = serializers.CharField()

    quantity = serializers.IntegerField()


# ==========================================
# CART SUMMARY
# ==========================================

class CartSummarySerializer(serializers.Serializer):

    items = CartItemSerializer(many=True)

    subtotal = serializers.FloatField()

    shipping = serializers.FloatField()

    total = serializers.FloatField()

    cart_count = serializers.IntegerField()


# ==========================================
# ADD TO CART
# ==========================================

class AddToCartSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()

    selected_size = serializers.CharField()

    quantity = serializers.IntegerField(
        required=False,
        default=1
    )


# ==========================================
# UPDATE CART
# ==========================================

class UpdateCartSerializer(serializers.Serializer):

    item_key = serializers.CharField()