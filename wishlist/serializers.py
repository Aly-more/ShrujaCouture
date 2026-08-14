from rest_framework import serializers


# ==========================================
# WISHLIST ITEM
# ==========================================

class WishlistItemSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()

    name = serializers.CharField()

    price = serializers.FloatField()

    discount_price = serializers.FloatField(
        allow_null=True
    )

    image = serializers.CharField()

    slug = serializers.CharField()


# ==========================================
# WISHLIST RESPONSE
# ==========================================

class WishlistSerializer(serializers.Serializer):

    items = WishlistItemSerializer(many=True)

    wishlist_count = serializers.IntegerField()


# ==========================================
# WISHLIST STATUS
# ==========================================

class WishlistStatusSerializer(serializers.Serializer):

    wishlist_ids = serializers.ListField(

        child=serializers.IntegerField()

    )

    wishlist_count = serializers.IntegerField()


# ==========================================
# TOGGLE REQUEST
# ==========================================

class ToggleWishlistSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()


# ==========================================
# REMOVE REQUEST
# ==========================================

class RemoveWishlistSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()



# ==========================================
# MOVE FROM CART
# ==========================================

class MoveFromCartSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()

    item_key = serializers.CharField()