from wishlist.models import Wishlist
from products.models import Product, ProductVariant
from .utils import calculate_cart_totals


# ==========================================
# GET CART
# ==========================================

def get_cart(request):

    return request.session.get("cart", {})


# ==========================================
# SAVE CART
# ==========================================

def save_cart(request, cart):

    request.session["cart"] = cart

    request.session.modified = True


# ==========================================
# CART COUNT
# ==========================================

def get_cart_count(cart):

    return sum(

        item["quantity"]

        for item in cart.values()

    )


# ==========================================
# CART KEY
# ==========================================

def get_cart_key(product_id, size):

    return f"{product_id}_{size}"


# ==========================================
# PRODUCT PRICE
# ==========================================

def get_product_price(product):

    if product.discount_price:

        return float(product.discount_price)

    return float(product.price)

# ==========================================
# ADD ITEM TO CART
# ==========================================

def add_item_to_cart(

    request,

    product,

    variant,

    quantity=1

):

    cart = get_cart(request)

    cart_key = get_cart_key(

        product.id,

        variant.size

    )

    price = get_product_price(product)

    # ==========================================
    # CURRENT QUANTITY
    # ==========================================

    current_quantity = 0

    if cart_key in cart:

        current_quantity = cart[cart_key]["quantity"]

    # ==========================================
    # STOCK VALIDATION
    # ==========================================

    if current_quantity + quantity > variant.stock:

        if request.user.is_authenticated:

            wishlist_count = Wishlist.objects.filter(

                user=request.user

            ).count()

        else:

            if not request.session.session_key:

                request.session.create()

            wishlist_count = Wishlist.objects.filter(

                session_key=request.session.session_key

            ).count()

        # ==========================================
        # FRIENDLY STOCK MESSAGE
        # ==========================================

        if variant.stock == 0:

            message = "Sorry, this item is out of stock."

        elif variant.stock == 1:

            message = "Sorry, only 1 piece is available."

        else:

            message = f"Sorry, only {variant.stock} pieces are available."

        return {

            "success": False,

            "message": message,

            "cart": cart,

            "wishlist_count": wishlist_count,

        }

    # ==========================================
    # ADD / UPDATE CART
    # ==========================================

    if cart_key in cart:

        cart[cart_key]["quantity"] += quantity

    else:

        cart[cart_key] = {

            "product_id": product.id,

            "variant_id": variant.id,

            "slug": product.slug,

            "name": product.name,

            "price": price,

            "image": product.main_image.url,

            "size": variant.size,

            "quantity": quantity,

        }

    save_cart(request, cart)

    # ==========================================
    # REMOVE FROM WISHLIST
    # ==========================================

    if request.user.is_authenticated:

        Wishlist.objects.filter(

            user=request.user,

            product=product

        ).delete()

        wishlist_count = Wishlist.objects.filter(

            user=request.user

        ).count()

    else:

        if not request.session.session_key:

            request.session.create()

        Wishlist.objects.filter(

            session_key=request.session.session_key,

            product=product

        ).delete()

        wishlist_count = Wishlist.objects.filter(

            session_key=request.session.session_key

        ).count()

    return {

        "success": True,

        "cart": cart,

        "wishlist_count": wishlist_count

    }

# ==========================================
# INCREASE QUANTITY
# ==========================================

def increase_cart_quantity(request, item_key):

    cart = get_cart(request)

    if item_key not in cart:

        return {

            "success": False,

            "message": "Item not found."

        }

    item = cart[item_key]

    variant = Product.objects.get(

        id=item["product_id"]

    ).variants.get(

        size=item["size"]

    )

    # ==========================================
    # STOCK VALIDATION
    # ==========================================

    if item["quantity"] >= variant.stock:

        return {

            "success": False,

            "message": f"Only {variant.stock} piece{'s' if variant.stock > 1 else ''} available."

        }

    item["quantity"] += 1

    save_cart(request, cart)

    return {

        "success": True

    }

# ==========================================
# DECREASE QUANTITY
# ==========================================

def decrease_cart_quantity(request, item_key):

    cart = get_cart(request)

    if item_key in cart:

        if cart[item_key]["quantity"] > 1:

            cart[item_key]["quantity"] -= 1

        else:

            del cart[item_key]

        save_cart(request, cart)

    return cart


# ==========================================
# REMOVE ITEM
# ==========================================

def remove_item_from_cart(request, item_key):

    cart = get_cart(request)

    if item_key in cart:

        del cart[item_key]

        save_cart(request, cart)

    return cart

# ==========================================
# CHANGE CART SIZE
# ==========================================
def change_cart_size(request, item_key, new_size):

    cart = get_cart(request)

    if item_key not in cart:

        return {

            "success": False,

            "message": "Cart item not found."

        }

    item = cart[item_key]

    product = Product.objects.get(

        id=item["product_id"]

    )

    try:

        variant = product.variants.get(

            size=new_size

        )

    except ProductVariant.DoesNotExist:

        return {

            "success": False,

            "message": "Selected size is unavailable."

        }

    # ==========================================
    # SAME SIZE SELECTED
    # ==========================================

    if item["size"] == new_size:

        return {

            "success": True,

            "merged": False,

            "quantity_adjusted": False,

        }

    # ==========================================
    # CREATE NEW KEY
    # ==========================================

    new_key = get_cart_key(

        product.id,

        new_size

    )

    quantity_adjusted = False

    adjusted_quantity = item["quantity"]

    merged = False

    removed_item_key = None

    updated_item_key = new_key

    # ==========================================
    # MERGE WITH EXISTING ITEM
    # ==========================================

    if new_key in cart:

        existing_item = cart[new_key]

        combined_quantity = (

            existing_item["quantity"]

            + item["quantity"]

        )

        if combined_quantity > variant.stock:

            combined_quantity = variant.stock

            quantity_adjusted = True

        existing_item["quantity"] = combined_quantity

        adjusted_quantity = combined_quantity

        merged = True

        removed_item_key = item_key

        del cart[item_key]

    # ==========================================
    # CHANGE SIZE ONLY
    # ==========================================

    else:

        if item["quantity"] > variant.stock:

            adjusted_quantity = variant.stock

            quantity_adjusted = True

        cart[new_key] = {

            **item,

            "variant_id": variant.id,

            "size": new_size,

            "quantity": adjusted_quantity,

        }

        del cart[item_key]

    save_cart(request, cart)

    return {

        "success": True,

        "merged": merged,

        "removed_item_key": removed_item_key,

        "updated_item_key": updated_item_key,

        "quantity_adjusted": quantity_adjusted,

        "adjusted_quantity": adjusted_quantity,

    }

# ==========================================
# CLEAR CART
# ==========================================

def clear_cart_items(request):

    save_cart(request, {})

    return {}


# ==========================================
# CART SUMMARY
# ==========================================

def get_cart_summary(request):

    cart = get_cart(request)

    totals = calculate_cart_totals(cart)

    return {

        "items": [

            {

                "item_key": key,

                **item

            }

            for key, item in cart.items()

        ],

        "subtotal": totals["subtotal"],

        "shipping": totals["shipping"],

        "total": totals["total"],

        "cart_count": get_cart_count(cart),

    }