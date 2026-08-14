from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Wishlist
from products.models import Product


# ==========================================
# GET SESSION KEY
# ==========================================

def get_session_key(request):

    if not request.session.session_key:

        request.session.create()

    return request.session.session_key


# ==========================================
# WISHLIST PAGE
# ==========================================

# ==========================================
# WISHLIST PAGE
# ==========================================

def wishlist(request):

    if request.user.is_authenticated:

        wishlist_items = (

            Wishlist.objects
            .select_related("product")
            .prefetch_related("product__variants")
            .filter(
                user=request.user
            )

        )

    else:

        wishlist_items = (

            Wishlist.objects
            .select_related("product")
            .prefetch_related("product__variants")
            .filter(
                session_key=get_session_key(request)
            )

        )

    context = {

        "wishlist_items": wishlist_items,

    }

    print(

        list(

            wishlist_items.values(

                "product__name",

                "session_key",

                "user_id"

            )

        )

    )

    return render(

        request,

        "wishlist.html",

        context

    )

def wishlist_status(request):

    if request.user.is_authenticated:

        wishlist = Wishlist.objects.filter(
            user=request.user
        )

    else:

        wishlist = Wishlist.objects.filter(
            session_key=get_session_key(request)
        )

    wishlist_ids = list(

        wishlist.values_list(
            "product_id",
            flat=True
        )

    )

    return JsonResponse({

        "wishlist_ids": wishlist_ids,

        "wishlist_count": wishlist.count()

    })

# ==========================================
# TOGGLE WISHLIST
# ==========================================

@require_POST
def toggle_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True,
        is_active=True
    )

    if request.user.is_authenticated:

        wishlist_item, created = Wishlist.objects.get_or_create(

            user=request.user,

            product=product

        )

        if not created:

            wishlist_item.delete()

            action = "removed"

        else:

            action = "added"

        wishlist_count = Wishlist.objects.filter(

            user=request.user

        ).count()

    else:

        session_key = get_session_key(request)

        wishlist_item, created = Wishlist.objects.get_or_create(

            session_key=session_key,

            product=product

        )

        if not created:

            wishlist_item.delete()

            action = "removed"

        else:

            action = "added"

        wishlist_count = Wishlist.objects.filter(

            session_key=session_key

        ).count()

    return JsonResponse({

        "success": True,

        "action": action,

        "wishlist_count": wishlist_count,

        "product_id": product.id

    })


# ==========================================
# REMOVE FROM WISHLIST
# ==========================================

@require_POST
def remove_from_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.user.is_authenticated:

        Wishlist.objects.filter(
            user=request.user,
            product=product
        ).delete()

        wishlist = Wishlist.objects.filter(
            user=request.user
        )

    else:

        Wishlist.objects.filter(
            session_key=get_session_key(request),
            product=product
        ).delete()

        wishlist = Wishlist.objects.filter(
            session_key=get_session_key(request)
        )

    return JsonResponse({

        "success": True,

        "wishlist_count": wishlist.count()

    })