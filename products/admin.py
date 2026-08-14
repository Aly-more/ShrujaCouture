from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Collection,
    ProductLabel,
    Product,
    ProductImage,
    ProductVariant,
    ContactMessage,
)


# =====================================
# CATEGORY
# =====================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# =====================================
# COLLECTION
# =====================================

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# =====================================
# PRODUCT LABEL
# =====================================

@admin.register(ProductLabel)
class ProductLabelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# =====================================
# INLINE GALLERY
# =====================================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = "Gallery Image"
    verbose_name_plural = "Gallery Images"


# =====================================
# INLINE VARIANTS
# =====================================

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    verbose_name = "Variant"
    verbose_name_plural = "Product Variants"


# =====================================
# PRODUCT
# =====================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "category",
        "price",
        "available",
        "is_active",
    )

    list_filter = (
        "category",
        "available",
        "is_active",
        "collections",
        "labels",
    )

    search_fields = (
        "name",
        "brand",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    filter_horizontal = (
        "collections",
        "labels",
    )

    fieldsets = (

        ("Basic Information", {

            "fields": (
                "name",
                "slug",
                "brand",
                "category",
                "collections",
                "labels",
            )

        }),

        ("Pricing", {

            "fields": (
                "price",
                "discount_price",
            )

        }),

        ("Images", {

            "fields": (
                "main_image",
                "hover_image",
            )

        }),

        ("Description", {

            "fields": (
                "description",
            )

        }),

        ("Status", {

            "fields": (
                "available",
                "is_active",
            )

        }),

    )

    inlines = [
        ProductImageInline,
        ProductVariantInline,
    ]

    def image_preview(self, obj):

        if obj.main_image:

            return format_html(
                '<img src="{}" style="height:70px;border-radius:10px;" />',
                obj.main_image.url
            )

        return "-"

    image_preview.short_description = "Preview"


# =====================================
# PRODUCT GALLERY
# =====================================

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "image",
    )

    search_fields = (
        "product__name",
    )


# =====================================
# PRODUCT VARIANTS
# =====================================

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "size",
        "color",
        "stock",
        "sku",
    )

    list_filter = (
        "size",
        "color",
    )

    search_fields = (
        "product__name",
        "sku",
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "email",
        "subject",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "subject",
    )

    readonly_fields = (
        "created_at",
    )