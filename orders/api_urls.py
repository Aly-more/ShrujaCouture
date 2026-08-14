from django.urls import path

from .api_views import (
    PlaceOrderAPIView,
    MyOrdersAPIView,
    OrderDetailAPIView,
    CancelOrderAPIView,
)

urlpatterns = [

    path(
        "place/",
        PlaceOrderAPIView.as_view(),
        name="place_order_api",
    ),

    path(
        "",
        MyOrdersAPIView.as_view(),
        name="my_orders_api",
    ),

    path(
        "<int:pk>/",
        OrderDetailAPIView.as_view(),
        name="order_detail_api",
    ),

    path(
        "<int:pk>/cancel/",
        CancelOrderAPIView.as_view(),
        name="cancel_order_api",
    ),
]