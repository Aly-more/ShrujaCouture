from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Product

from .services import (
    get_wishlist,
    get_wishlist_ids,
    get_wishlist_count,
    toggle_wishlist,
    remove_wishlist_item,
    move_from_cart,
)

from .serializers import (
    WishlistSerializer,
    WishlistStatusSerializer,
    ToggleWishlistSerializer,
    RemoveWishlistSerializer,
    MoveFromCartSerializer,
)


# ==========================================
# WISHLIST API
# ==========================================

class WishlistAPIView(APIView):

    def get(self, request):

        wishlist = get_wishlist(request)

        items = []

        for item in wishlist:

            product = item.product

            items.append({

                "product_id": product.id,

                "name": product.name,

                "price": float(product.price),

                "discount_price": (
                    float(product.discount_price)
                    if product.discount_price
                    else None
                ),

                "image": product.main_image.url,

                "slug": product.slug,

            })

        data = {

            "items": items,

            "wishlist_count": get_wishlist_count(request),

        }

        serializer = WishlistSerializer(data)

        return Response(

            {

                "success": True,

                "wishlist": serializer.data,

            },

            status=status.HTTP_200_OK

        )


# ==========================================
# WISHLIST STATUS API
# ==========================================

class WishlistStatusAPIView(APIView):

    def get(self, request):

        data = {

            "wishlist_ids": get_wishlist_ids(request),

            "wishlist_count": get_wishlist_count(request),

        }

        serializer = WishlistStatusSerializer(data)

        return Response(

            {

                "success": True,

                "wishlist": serializer.data,

            },

            status=status.HTTP_200_OK

        )


# ==========================================
# TOGGLE WISHLIST
# ==========================================

class ToggleWishlistAPIView(APIView):

    def post(self, request):

        serializer = ToggleWishlistSerializer(

            data=request.data

        )

        serializer.is_valid(

            raise_exception=True

        )

        product = get_object_or_404(

            Product,

            id=serializer.validated_data["product_id"],

            available=True,

            is_active=True

        )

        data = toggle_wishlist(

            request,

            product

        )

        return Response(

            {

                "success": True,

                "wishlist": data

            },

            status=status.HTTP_200_OK

        )

# ==========================================
# REMOVE WISHLIST ITEM
# ==========================================

class RemoveWishlistAPIView(APIView):

    def delete(self, request):

        serializer = RemoveWishlistSerializer(

            data=request.data

        )

        serializer.is_valid(

            raise_exception=True

        )

        product = get_object_or_404(

            Product,

            id=serializer.validated_data["product_id"]

        )

        data = remove_wishlist_item(

            request,

            product

        )

        return Response(

                {

                    "success": True,

                    "wishlist": data

                },

                status=status.HTTP_200_OK

            )

# ==========================================
# MOVE FROM CART
# ==========================================

class MoveFromCartAPIView(APIView):

    def post(self, request):

        serializer = MoveFromCartSerializer(

            data=request.data

        )

        serializer.is_valid(

            raise_exception=True

        )

        data = move_from_cart(

            request,

            serializer.validated_data["product_id"],

            serializer.validated_data["item_key"]

        )

        return Response(

            {

                "success": True,

                "wishlist": data

            },

            status=status.HTTP_200_OK

        )