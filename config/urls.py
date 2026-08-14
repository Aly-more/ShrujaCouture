"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # ==========================================
    # ADMIN
    # ==========================================

    path(
        "admin/",
        admin.site.urls
    ),


    # ==========================================
    # PRODUCTS / HOME / SHOP
    # ==========================================

    path(
    "",
    include(("products.urls", "products"), namespace="products")
),

    # ==========================================
    # CART
    # ==========================================

    path(
        "cart/",
        include("cart.urls")
    ),

    path(
        "api/cart/",
        include("cart.api_urls")
    ),


    # ==========================================
    # CHECKOUT
    # ==========================================

    path(
        "checkout/",
        include("checkout.urls")
    ),

    path(
        "api/checkout/",
        include("checkout.api_urls")
    ),


    # ==========================================
    # WISHLIST
    # ==========================================

    path(
        "wishlist/",
        include("wishlist.urls")
    ),

    path(
        "api/wishlist/",
        include("wishlist.api_urls")
    ),


    # ==========================================
    # CUSTOMER ACCOUNT — WEBSITE
    # ==========================================

    path(
        "account/",
        include("accounts.urls")
    ),


    # ==========================================
    # CUSTOMER ACCOUNT — API
    # ==========================================

    path(
        "api/accounts/",
        include("accounts.api_urls")
    ),


    # ==========================================
    # ORDERS
    # ==========================================

    path(
        "orders/",
        include("orders.urls")
    ),

    path(
        "api/orders/",
        include("orders.api_urls")
    ),


    # ==========================================
    # PAYMENTS API
    # ==========================================

    path(
        "api/payments/",
        include("payments.api_urls")
    ),


    # ==========================================
    # PRODUCTS API
    # ==========================================

    path(
        "api/products/",
        include("products.api_urls")
    ),

]


# ==========================================
# MEDIA FILES — DEVELOPMENT
# ==========================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )