from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
)


# ==========================================
# PRODUCT LIST
# ==========================================

class ProductListAPIView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            is_active=True,
            available=True,
        )

        serializer = ProductListSerializer(
            products,
            many=True,
        )

        return Response(
            {
                "success": True,
                "count": products.count(),
                "products": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# PRODUCT DETAIL
# ==========================================

class ProductDetailAPIView(APIView):

    def get(self, request, slug):

        product = get_object_or_404(
            Product,
            slug=slug,
            is_active=True,
            available=True,
        )

        serializer = ProductDetailSerializer(
            product
        )

        return Response(
            {
                "success": True,
                "product": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# PRODUCT SEARCH
# ==========================================

class ProductSearchAPIView(APIView):

    def get(self, request):

        query = request.GET.get(
            "q",
            ""
        ).strip()

        # ------------------------------------------
        # EMPTY SEARCH
        # ------------------------------------------

        if not query:

            return Response(
                {
                    "success": True,
                    "count": 0,
                    "products": [],
                },
                status=status.HTTP_200_OK,
            )


        # ------------------------------------------
        # SEARCH PRODUCTS
        # ------------------------------------------

        products = Product.objects.filter(
            is_active=True,
            available=True,
        ).filter(

            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(collections__name__icontains=query) |
            Q(labels__name__icontains=query)

        ).distinct()[:8]


        # ------------------------------------------
        # BUILD SEARCH RESULTS
        # ------------------------------------------

        results = []

        for product in products:

            image_url = ""

            if product.main_image:

                image_url = request.build_absolute_uri(
                    product.main_image.url
                )


            # --------------------------------------
            # PRODUCT DETAIL URL
            # --------------------------------------

            product_url = reverse(
                "products:product_detail",
                kwargs={
                    "slug": product.slug
                }
            )


            # --------------------------------------
            # PRODUCT DATA
            # --------------------------------------

            results.append(
                {
                    "id": product.id,

                    "name": product.name,

                    "slug": product.slug,

                    "price": str(product.price),

                    "discount_price": (
                        str(product.discount_price)
                        if product.discount_price
                        else None
                    ),

                    "image": image_url,

                    "url": product_url,
                }
            )


        # ------------------------------------------
        # RESPONSE
        # ------------------------------------------

        return Response(
            {
                "success": True,
                "count": len(results),
                "products": results,
            },
            status=status.HTTP_200_OK,
        )