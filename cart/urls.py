from django.urls import path
from . import views

urlpatterns = [

    path("", views.cart, name="cart"),

    path("add/<int:product_id>/",
         views.add_to_cart,
         name="add_to_cart"),

     path(
     "quick-add/",
     views.quick_add_to_cart,
     name="quick_add_to_cart"),

    path("increase/<str:item_key>/",
         views.increase_quantity,
         name="increase_quantity"),

    path("decrease/<str:item_key>/",
         views.decrease_quantity,
         name="decrease_quantity"),

    path("remove/<str:item_key>/",
         views.remove_item,
         name="remove_item"),

    path(
          "change-size/",
          views.change_cart_size,
          name="change_cart_size",
          ),

    path("clear/",
         views.clear_cart,
         name="clear_cart"),
]