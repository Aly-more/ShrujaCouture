from django.urls import path

from .api_views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductSearchAPIView,
)

from .views import product_sizes


urlpatterns = [

    # ==========================================
    # PRODUCT LIST
    # ==========================================

    path(
        "",
        ProductListAPIView.as_view(),
        name="product-list",
    ),


    # ==========================================
    # PRODUCT SEARCH
    # ==========================================

    path(
        "search/",
        ProductSearchAPIView.as_view(),
        name="product-search",
    ),

    # ==========================================
    # PRODUCT SIZES
    # ==========================================

    path(
        "<int:product_id>/sizes/",
        product_sizes,
        name="product-sizes",
    ),


    path(
        "<slug:slug>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),

]