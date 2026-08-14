from decimal import Decimal
from uuid import uuid4

from django.db import transaction
from django.shortcuts import get_object_or_404

from accounts.models import Address
from cart.services import get_cart
from products.models import Product, ProductVariant

from .models import Order, OrderItem


# ==========================================
# GENERATE ORDER NUMBER
# ==========================================

def generate_order_number():

    return f"SC-{uuid4().hex[:10].upper()}"


# ==========================================
# PLACE ORDER
# ==========================================

@transaction.atomic
def place_order(request, validated_data):

    user = request.user

    address = get_object_or_404(
        Address,
        id=validated_data["address_id"],
        user=user,
    )

    # ==========================================
    # DEBUG
    # ==========================================

    print("\n" + "=" * 60)
    print("PLACE ORDER API")
    print("Session Key :", request.session.session_key)
    print("Session Cart:", request.session.get("cart"))
    print("=" * 60 + "\n")

    cart = get_cart(request)

    if not cart:
        raise ValueError("Your cart is empty.")

    subtotal = Decimal("0.00")

    order = Order.objects.create(

        order_number=generate_order_number(),

        user=user,

        shipping_address=address,

        customer_name=address.full_name,

        email=user.email,

        phone=address.phone_number,

        address=f"{address.address_line_1}, {address.address_line_2}".strip(", "),

        city=address.city,

        state=address.state,

        pincode=address.postal_code,

        subtotal=Decimal("0.00"),

        shipping_charge=Decimal("0.00"),

        total=Decimal("0.00"),

        notes=validated_data.get("notes", ""),

    )

    for item in cart.values():

        product = get_object_or_404(
            Product,
            id=item["product_id"],
            available=True,
            is_active=True,
        )

        variant = get_object_or_404(
            ProductVariant,
            id=item["variant_id"],
            product=product,
        )

        quantity = item["quantity"]

        if quantity > variant.stock:
            raise ValueError(
                f"Only {variant.stock} item(s) left for {product.name} ({variant.size})."
            )

        price = (
            product.discount_price
            if product.discount_price
            else product.price
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            variant=variant,
            quantity=quantity,
            price=price,
        )

        subtotal += price * quantity

    shipping = Decimal("0.00")

    order.subtotal = subtotal

    order.shipping_charge = shipping

    order.total = subtotal + shipping

    order.save(
        update_fields=[
            "subtotal",
            "shipping_charge",
            "total",
        ]
    )

    # ==========================================
    # DO NOT CLEAR CART HERE
    # Cart will be cleared only after
    # successful payment verification.
    # ==========================================

    return order