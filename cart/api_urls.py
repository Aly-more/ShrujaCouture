from django.urls import path

from .api_views import (
    CartAPIView,
    AddToCartAPIView,
    IncreaseQuantityAPIView,
    DecreaseQuantityAPIView,
    RemoveItemAPIView,
    ClearCartAPIView,
)
urlpatterns = [

    path(
        "",
        CartAPIView.as_view(),
        name="cart_api"
    ),

    path(
        "add/",
        AddToCartAPIView.as_view(),
        name="cart_add_api"
    ),

    path(
        "increase/",
        IncreaseQuantityAPIView.as_view(),
        name="cart_increase_api"
    ),

    path(
    "decrease/",
    DecreaseQuantityAPIView.as_view(),
    name="cart_decrease_api"
),

path(
    "remove/",
    RemoveItemAPIView.as_view(),
    name="cart_remove_api"
),

path(
    "clear/",
    ClearCartAPIView.as_view(),
    name="cart_clear_api"
),

]