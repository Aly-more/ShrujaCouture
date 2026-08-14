from rest_framework import serializers

from .models import (
    Product,
    ProductImage,
    ProductVariant,
)


# ==========================================
# PRODUCT VARIANT
# ==========================================

class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductVariant

        fields = (
            "id",
            "size",
            "color",
            "stock",
            "sku",
        )


# ==========================================
# PRODUCT GALLERY IMAGE
# ==========================================

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductImage

        fields = (
            "id",
            "image",
        )


# ==========================================
# PRODUCT LIST
# ==========================================

class ProductListSerializer(serializers.ModelSerializer):

    display_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    has_discount = serializers.BooleanField(
        read_only=True
    )

    total_stock = serializers.IntegerField(
        read_only=True
    )

    sold_out = serializers.BooleanField(
        read_only=True
    )

    class Meta:

        model = Product

        fields = (
            "id",
            "name",
            "slug",
            "brand",
            "price",
            "discount_price",
            "display_price",
            "has_discount",
            "main_image",
            "hover_image",
            "total_stock",
            "sold_out",
        )


# ==========================================
# PRODUCT DETAIL
# ==========================================

class ProductDetailSerializer(serializers.ModelSerializer):

    variants = ProductVariantSerializer(
        many=True,
        read_only=True,
    )

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    display_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    has_discount = serializers.BooleanField(
        read_only=True,
    )

    total_stock = serializers.IntegerField(
        read_only=True,
    )

    sold_out = serializers.BooleanField(
        read_only=True,
    )

    low_stock = serializers.BooleanField(
        read_only=True,
    )

    in_stock = serializers.BooleanField(
        read_only=True,
    )

    class Meta:

        model = Product

        fields = (
            "id",
            "name",
            "slug",
            "brand",
            "description",
            "price",
            "discount_price",
            "display_price",
            "has_discount",
            "main_image",
            "hover_image",
            "variants",
            "images",
            "total_stock",
            "sold_out",
            "low_stock",
            "in_stock",
            "created_at",
        )