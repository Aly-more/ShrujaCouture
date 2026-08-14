from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import get_cart_summary
from .serializers import CartSummarySerializer

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Product, ProductVariant

from .services import (
    add_item_to_cart,
    get_cart_summary,
    increase_cart_quantity,
    decrease_cart_quantity,
    remove_item_from_cart,
    clear_cart_items,
)

from .serializers import (
    CartSummarySerializer,
    AddToCartSerializer,
    UpdateCartSerializer,
)


# ==========================================
# CART SUMMARY API
# ==========================================

class CartAPIView(APIView):

    def get(self, request):

        summary = get_cart_summary(request)

        serializer = CartSummarySerializer(summary)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
# ==========================================
# ADD TO CART API
# ==========================================

class AddToCartAPIView(APIView):

    def post(self, request):

        serializer = AddToCartSerializer(

            data=request.data

        )

        serializer.is_valid(

            raise_exception=True

        )

        product_id = serializer.validated_data["product_id"]

        selected_size = serializer.validated_data["selected_size"]

        quantity = serializer.validated_data["quantity"]

        product = get_object_or_404(

            Product,

            id=product_id,

            available=True,

            is_active=True

        )

        variant = get_object_or_404(

            ProductVariant,

            product=product,

            size=selected_size

        )

        # ==========================================
        # OUT OF STOCK
        # ==========================================

        if variant.stock <= 0:

            return Response(

                {

                    "success": False,

                    "message": "Out of Stock"

                },

                status=status.HTTP_400_BAD_REQUEST

            )

        # ==========================================
        # ADD TO CART
        # ==========================================

        result = add_item_to_cart(

            request,

            product,

            variant,

            quantity

        )

        # ==========================================
        # STOCK LIMIT REACHED
        # ==========================================

        if not result["success"]:

            return Response(

                {

                    "success": False,

                    "message": result["message"]

                },

                status=status.HTTP_400_BAD_REQUEST

            )

        summary = get_cart_summary(request)

        response_serializer = CartSummarySerializer(

            summary

        )

        return Response(

            {

                "success": True,

                "message": "Added to Bag",

                "cart": response_serializer.data,

                "cart_count": summary["cart_count"],

                "wishlist_count": result["wishlist_count"]

            },

            status=status.HTTP_200_OK

        )
    
# ==========================================
# INCREASE QUANTITY API
# ==========================================

class IncreaseQuantityAPIView(APIView):

    def patch(self, request):

        serializer = UpdateCartSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        item_key = serializer.validated_data["item_key"]

        result = increase_cart_quantity(

            request,

            item_key

        )

        summary = get_cart_summary(request)

        response_serializer = CartSummarySerializer(

            summary

        )

        if not result["success"]:

            return Response(

                {

                    "success": False,

                    "message": result["message"],

                    "cart": response_serializer.data,

                },

                status=status.HTTP_400_BAD_REQUEST,

            )

        return Response(

            {

                "success": True,

                "message": "Quantity updated.",

                "cart": response_serializer.data,

            },

            status=status.HTTP_200_OK,

        )
                
# ==========================================
# DECREASE QUANTITY API
# ==========================================

class DecreaseQuantityAPIView(APIView):

    def patch(self, request):

        serializer = UpdateCartSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        item_key = serializer.validated_data["item_key"]

        decrease_cart_quantity(
            request,
            item_key
        )

        summary = get_cart_summary(request)

        response_serializer = CartSummarySerializer(
            summary
        )

        return Response(
    {
        "success": True,
        "message": "Quantity updated.",
        "cart": response_serializer.data,
    },
    status=status.HTTP_200_OK,
)
    

# ==========================================
# REMOVE ITEM API
# ==========================================

class RemoveItemAPIView(APIView):

    def delete(self, request):

        serializer = UpdateCartSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        item_key = serializer.validated_data["item_key"]

        remove_item_from_cart(
            request,
            item_key
        )

        summary = get_cart_summary(request)

        response_serializer = CartSummarySerializer(
            summary
        )

        return Response(
    {
        "success": True,
        "message": "Item removed from cart.",
        "cart": response_serializer.data,
    },
    status=status.HTTP_200_OK,
)
    
# ==========================================
# CLEAR CART API
# ==========================================

class ClearCartAPIView(APIView):

    def delete(self, request):

        clear_cart_items(request)

        summary = get_cart_summary(request)

        response_serializer = CartSummarySerializer(
            summary
        )

        return Response(
        {
            "success": True,
            "message": "Cart cleared.",
            "cart": response_serializer.data,
        },
        status=status.HTTP_200_OK,
    )