from django.urls import path
from . import views

from .views import (
    checkout,
    order_success,
)

urlpatterns = [

    path(
        "",
        checkout,
        name="checkout",
    ),

    path(
        "order-success/",
        order_success,
        name="order_success",
    ),

    path(

    "address-list/",
    views.address_list_partial,
    name="checkout-address-list",
),

]