from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import razorpay
from cart.services import clear_cart_items
from orders.email_service import send_order_confirmation_email

from orders.models import Order

from .serializers import (
    CreatePaymentSerializer,
    VerifyPaymentSerializer,
)

from .services import client


class CreatePaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CreatePaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        order = get_object_or_404(
            Order,
            id=serializer.validated_data["order_id"],
            user=request.user,
        )

        razorpay_order = client.order.create(
            {
                "amount": int(order.total * 100),
                "currency": "INR",
                "receipt": order.order_number,
                "payment_capture": 1,
            }
        )

        order.razorpay_order_id = razorpay_order["id"]

        order.save(update_fields=["razorpay_order_id"])

        return Response(
            {
                "success": True,
                "message": "Razorpay order created successfully.",

                "payment": {

                    "order_id": order.id,

                    "razorpay_order_id": razorpay_order["id"],

                    "amount": razorpay_order["amount"],

                    "currency": razorpay_order["currency"],

                    "key": settings.RAZORPAY_KEY_ID,

                }

            },
            status=status.HTTP_200_OK,
        )
    
class VerifyPaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = VerifyPaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        razorpay_order_id = serializer.validated_data["razorpay_order_id"]

        razorpay_payment_id = serializer.validated_data["razorpay_payment_id"]

        razorpay_signature = serializer.validated_data["razorpay_signature"]

        order = get_object_or_404(
            Order,
            razorpay_order_id=razorpay_order_id,
            user=request.user,
        )

        try:

            client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                }
            )

            order.razorpay_payment_id = razorpay_payment_id

            order.razorpay_signature = razorpay_signature

            order.payment_status = Order.PaymentStatus.PAID

            order.status = Order.OrderStatus.PENDING

            order.save(
                update_fields=[
                    "razorpay_payment_id",
                    "razorpay_signature",
                    "payment_status",
                    "status",
                ]
            )

            # ==========================================
            # SEND CONFIRMATION EMAIL
            # ==========================================

            send_order_confirmation_email(order)

            # ==========================================
            # REDUCE PRODUCT STOCK
            # ==========================================

            for item in order.items.select_related("variant"):

                variant = item.variant

                variant.stock = max(
                    0,
                    variant.stock - item.quantity
                )


                variant.save(update_fields=["stock"])

            # ==========================================
            # CLEAR CART
            # ==========================================

            clear_cart_items(request)
            
            request.session["last_order_id"] = order.id
            return Response(
                {
                    "success": True,
                    "message": "Payment verified successfully.",
                },
                status=status.HTTP_200_OK,
            )

        except razorpay.errors.SignatureVerificationError:

            order.payment_status = Order.PaymentStatus.FAILED

            order.save()

            return Response(
                {
                    "success": False,
                    "message": "Payment verification failed.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )