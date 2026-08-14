from django.urls import path

from .api_views import (
    CreateAddressAPIView,
    UpdateAddressAPIView,
    AddressListAPIView,
    DeleteAddressAPIView,
)

urlpatterns = [

    path(
        "address/create/",
        CreateAddressAPIView.as_view(),
        name="checkout-address-create",
    ),

    path(
        "address/<int:pk>/",
        UpdateAddressAPIView.as_view(),
        name="checkout-address-update",
    ),

    path(
        "addresses/",
        AddressListAPIView.as_view(),
        name="checkout-address-list",
    ),

    path(

    "address/<int:pk>/delete/",
    DeleteAddressAPIView.as_view(),
    name="checkout-address-delete",
),

]