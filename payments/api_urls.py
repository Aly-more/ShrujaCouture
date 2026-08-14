from django.urls import path

from .api_views import (
    CreatePaymentAPIView,
    VerifyPaymentAPIView,
)

urlpatterns = [

    path(
        "create/",
        CreatePaymentAPIView.as_view(),
        name="create_payment_api",
    ),

    path(
        "verify/",
        VerifyPaymentAPIView.as_view(),
        name="verify_payment_api",
    ),
]