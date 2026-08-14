from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from products.models import Product, ProductVariant

from .utils import calculate_cart_totals

from .services import (
    add_item_to_cart,
    get_cart,
    get_cart_count,
    increase_cart_quantity,
    decrease_cart_quantity,
    remove_item_from_cart,
    clear_cart_items,
)


# ==========================================
# CART PAGE
# ==========================================

def cart(request):

    cart = request.session.get("cart", {})

    print("\n" + "=" * 60)
    print("CART PAGE")
    print("Session Key :", request.session.session_key)
    print("Session Cart:", cart)
    print("=" * 60 + "\n")

    totals = calculate_cart_totals(cart)

    context = {

        "cart": cart,

        **totals,

    }

    return render(
        request,
        "cart.html",
        context
    )


# ==========================================
# ADD TO CART
# ==========================================

def add_to_cart(request, product_id):

    if request.method != "POST":

        return redirect("cart")

    product = get_object_or_404(

        Product,

        id=product_id

    )

    selected_size = request.POST.get("selected_size")

    quantity = int(

        request.POST.get(

            "quantity",

            1

        )

    )

    if not selected_size:

        return redirect(

            "product_detail",

            slug=product.slug

        )

    variant = get_object_or_404(

        ProductVariant,

        product=product,

        size=selected_size

    )

    # ==========================================
    # STOCK VALIDATION
    # ==========================================

    if quantity > variant.stock:

        messages.error(

            request,

            f"Only {variant.stock} item(s) available in stock."

        )

        return redirect(

            "product_detail",

            slug=product.slug

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

    if not result["success"]:

        messages.error(

            request,

            result["message"]

        )

        return redirect(

            "product_detail",

            slug=product.slug

        )

    return redirect("cart")


# ==========================================
# QUICK ADD
# ==========================================

@require_POST
def quick_add_to_cart(request):

    product_id = request.POST.get("product_id")

    selected_size = request.POST.get("selected_size")

    # ==========================================
    # PRODUCT
    # ==========================================

    product = get_object_or_404(

        Product,

        id=product_id,

        available=True,

        is_active=True

    )

    # ==========================================
    # SIZE NOT SELECTED
    # ==========================================

    if not selected_size:

        return JsonResponse({

            "success": False,

            "message": "Please select a size."

        })

    # ==========================================
    # VARIANT
    # ==========================================

    variant = get_object_or_404(

        ProductVariant,

        product=product,

        size=selected_size

    )

    # ==========================================
    # OUT OF STOCK
    # ==========================================

    if variant.stock <= 0:

        return JsonResponse({

            "success": False,

            "message": "Out of Stock"

        })

    # ==========================================
    # ADD TO CART
    # ==========================================

    result = add_item_to_cart(

        request,

        product,

        variant,

        1

    )

    if not result["success"]:

        return JsonResponse({

            "success": False,

            "message": result["message"]

        })

    cart_count = get_cart_count(

        result["cart"]

    )

    return JsonResponse({

        "success": True,

        "cart_count": cart_count,

        "wishlist_count": result["wishlist_count"]

    })


# ==========================================
# INCREASE QUANTITY
# ==========================================

def increase_quantity(request, item_key):

    increase_cart_quantity(

        request,

        item_key

    )

    return redirect("cart")


# ==========================================
# DECREASE QUANTITY
# ==========================================

def decrease_quantity(request, item_key):

    decrease_cart_quantity(

        request,

        item_key

    )

    return redirect("cart")


# ==========================================
# REMOVE ITEM
# ==========================================

def remove_item(request, item_key):

    remove_item_from_cart(

        request,

        item_key

    )

    return redirect("cart")


# ==========================================
# CLEAR CART
# ==========================================

def clear_cart(request):

    clear_cart_items(request)

    return redirect("cart")

@require_POST
def change_cart_size(request):

    item_key = request.POST.get("item_key")
    new_size = request.POST.get("size")

    from .services import (
        change_cart_size,
        get_cart_summary,
    )

    result = change_cart_size(
        request,
        item_key,
        new_size
    )

    if result["success"]:

        result["cart"] = get_cart_summary(request)

    return JsonResponse(result)