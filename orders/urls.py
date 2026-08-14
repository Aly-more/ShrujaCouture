from django.urls import path

from .views import (
    my_orders,
    order_detail,
    order_success,
)

app_name = "orders"

urlpatterns = [

    path(
        "",
        my_orders,
        name="my_orders",
    ),

    path(
        "success/",
        order_success,
        name="order_success",
    ),

    path(
        "<int:order_id>/",
        order_detail,
        name="order_detail",
    ),

]