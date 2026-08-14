from django.urls import path

from .api_views import (
    WishlistAPIView,
    WishlistStatusAPIView,
    ToggleWishlistAPIView,
    RemoveWishlistAPIView,
    MoveFromCartAPIView,
)

urlpatterns = [

    path(
        "",
        WishlistAPIView.as_view(),
        name="wishlist_api",
    ),

    path(
        "status/",
        WishlistStatusAPIView.as_view(),
        name="wishlist_status_api",
    ),

    path(
        "toggle/",
        ToggleWishlistAPIView.as_view(),
        name="wishlist_toggle_api",
    ),

    path(
        "remove/",
        RemoveWishlistAPIView.as_view(),
        name="wishlist_remove_api",
    ),

    path(
        "move-from-cart/",
        MoveFromCartAPIView.as_view(),
        name="wishlist_move_from_cart_api",
    ),

]