from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.wishlist,
        name="wishlist"
    ),

    path(
    "toggle/<int:product_id>/",
    views.toggle_wishlist,
    name="toggle_wishlist",
),

    path(
        "remove/<int:product_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist"
    ),

   path(
        "status/",
        views.wishlist_status,
        name="wishlist_status",
    ),

]