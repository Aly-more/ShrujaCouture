# ==========================================
# WISHLIST SERVICES
# ==========================================

from .models import Wishlist
from products.models import Product
from cart.services import (
    remove_item_from_cart,
    get_cart_key,
)


# ==========================================
# SESSION KEY
# ==========================================

def get_session_key(request):

    if not request.session.session_key:

        request.session.create()

    return request.session.session_key


# ==========================================
# GET WISHLIST
# ==========================================

def get_wishlist(request):

    if request.user.is_authenticated:

        return (

            Wishlist.objects
            .select_related("product")
            .prefetch_related("product__variants")
            .filter(
                user=request.user
            )

        )

    return (

        Wishlist.objects
        .select_related("product")
        .prefetch_related("product__variants")
        .filter(
            session_key=get_session_key(request)
        )

    )


# ==========================================
# GET WISHLIST COUNT
# ==========================================

def get_wishlist_count(request):

    return get_wishlist(request).count()


# ==========================================
# GET WISHLIST IDS
# ==========================================

def get_wishlist_ids(request):

    return list(

        get_wishlist(request).values_list(

            "product_id",

            flat=True

        )

    )


# ==========================================
# TOGGLE WISHLIST
# ==========================================

def toggle_wishlist(request, product):

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

    else:

        wishlist_item, created = Wishlist.objects.get_or_create(

            session_key=get_session_key(request),

            product=product

        )

        if not created:

            wishlist_item.delete()

            action = "removed"

        else:

            action = "added"

    return {

        "action": action,

        "wishlist_count": get_wishlist_count(request),

        "wishlist_ids": get_wishlist_ids(request),

    }


# ==========================================
# REMOVE FROM WISHLIST
# ==========================================

def remove_wishlist_item(request, product):

    if request.user.is_authenticated:

        Wishlist.objects.filter(

            user=request.user,

            product=product

        ).delete()

    else:

        Wishlist.objects.filter(

            session_key=get_session_key(request),

            product=product

        ).delete()

    return {

        "wishlist_count": get_wishlist_count(request),

        "wishlist_ids": get_wishlist_ids(request),

    }


# ==========================================
# MOVE FROM CART
# ==========================================

def move_from_cart(request, product, size):

    if request.user.is_authenticated:

        Wishlist.objects.get_or_create(

            user=request.user,

            product=product

        )

    else:

        Wishlist.objects.get_or_create(

            session_key=get_session_key(request),

            product=product

        )

    item_key = get_cart_key(

        product.id,

        size

    )

    remove_item_from_cart(

        request,

        item_key

    )

    return {

        "wishlist_count": get_wishlist_count(request),

        "wishlist_ids": get_wishlist_ids(request),

    }

# ==========================================
# MOVE FROM CART
# ==========================================

from cart.services import (
    get_cart,
    save_cart,
)

from .models import Wishlist

from products.models import Product


def move_from_cart(request, product_id, item_key):

    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:

        Wishlist.objects.get_or_create(

            user=request.user,

            product=product

        )

        wishlist = Wishlist.objects.filter(

            user=request.user

        )

    else:

        if not request.session.session_key:

            request.session.create()

        session_key = request.session.session_key

        Wishlist.objects.get_or_create(

            session_key=session_key,

            product=product

        )

        wishlist = Wishlist.objects.filter(

            session_key=session_key

        )

    cart = get_cart(request)

    cart.pop(item_key, None)

    save_cart(request, cart)

    return {

        "wishlist_count": wishlist.count(),

        "wishlist_ids": list(

            wishlist.values_list(

                "product_id",

                flat=True

            )

        )

    }