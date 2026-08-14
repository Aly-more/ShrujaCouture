from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import (
    PlaceOrderSerializer,
    OrderSerializer,
)
from .services import place_order


# ==========================================
# PLACE ORDER
# ==========================================

class PlaceOrderAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = PlaceOrderSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            order = place_order(
                request,
                serializer.validated_data
            )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        response_serializer = OrderSerializer(order)

        return Response(
            {
                "success": True,
                "message": "Order placed successfully.",
                "order": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


# ==========================================
# MY ORDERS
# ==========================================

class MyOrdersAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        orders = Order.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(
            {
                "success": True,
                "orders": serializer.data
            },
            status=status.HTTP_200_OK
        )


# ==========================================
# ORDER DETAILS
# ==========================================

class OrderDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, pk):

        order = get_object_or_404(

            Order,

            id=pk,

            user=request.user

        )

        serializer = OrderSerializer(
            order
        )

        return Response(
            {
                "success": True,
                "order": serializer.data
            },
            status=status.HTTP_200_OK
        )


# ==========================================
# CANCEL ORDER
# ==========================================

class CancelOrderAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        order = get_object_or_404(

            Order,

            id=pk,

            user=request.user

        )

        # Already Cancelled
        if order.status == Order.OrderStatus.CANCELLED:

            return Response(
                {
                    "success": False,
                    "message": "Order is already cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Can only cancel Pending or Confirmed orders
        if order.status not in [

            Order.OrderStatus.PENDING,

            Order.OrderStatus.CONFIRMED

        ]:

            return Response(
                {
                    "success": False,
                    "message": "This order can no longer be cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Restore stock
        for item in order.items.all():

            item.variant.stock += item.quantity

            item.variant.save(
                update_fields=["stock"]
            )

        # Update order
        order.status = Order.OrderStatus.CANCELLED

        order.save(
            update_fields=["status"]
        )

        serializer = OrderSerializer(order)

        return Response(
            {
                "success": True,
                "message": "Order cancelled successfully.",
                "order": serializer.data
            },
            status=status.HTTP_200_OK
        )