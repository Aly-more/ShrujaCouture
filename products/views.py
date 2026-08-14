from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Case, When, IntegerField

from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Category, Product, ProductVariant
from core.models import InstagramPost

from .forms import ContactMessageForm


# ==========================================
# HOME
# ==========================================

def home(request):

    categories = Category.objects.all()

    new_arrivals = Product.objects.filter(
        available=True,
        is_active=True,
        labels__name="New Arrival"
    ).distinct().order_by("-created_at")

    instagram_posts = InstagramPost.objects.filter(
        is_active=True
    ).order_by("display_order")[:6]

    context = {
        "categories": categories,
        "new_arrivals": new_arrivals,
        "instagram_posts": instagram_posts,
    }

    return render(request, "home.html", context)


# ==========================================
# SHOP
# ==========================================

def shop(request):

    products = Product.objects.filter(
        available=True,
        is_active=True
    ).order_by("-created_at")

    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
    }

    return render(
        request,
        "shop.html",
        context
    )


# ==========================================
# NEW ARRIVALS
# ==========================================
def new_arrivals(request):

    products = Product.objects.filter(
        available=True,
        is_active=True,
        labels__name="New Arrival"
    ).distinct().order_by("-created_at")

    context = {
        "products": products,
    }

    return render(
        request,
        "new_arrivals.html",
        context
    )


# ==========================================
# CATEGORY PRODUCTS
# ==========================================

def category_products(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    products = Product.objects.filter(
        category=category,
        available=True,
        is_active=True
    ).order_by("-created_at")

    categories = Category.objects.all()

    context = {
        "category": category,
        "products": products,
        "categories": categories,
    }

    return render(
        request,
        "category_products.html",
        context
    )


# ==========================================
# PRODUCT DETAILS
# ==========================================

def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        available=True,
        is_active=True
    )

    variants = ProductVariant.objects.filter(
        product=product
    ).order_by(
        Case(
            When(size="XS", then=0),
            When(size="S", then=1),
            When(size="M", then=2),
            When(size="L", then=3),
            When(size="XL", then=4),
            When(size="XXL", then=5),
            output_field=IntegerField(),
        )
    )

    # ==========================================
    # REMAINING STOCK AFTER CART
    # ==========================================

    cart = request.session.get("cart", {})

    for variant in variants:

        cart_key = f"{product.id}_{variant.size}"

        cart_quantity = cart.get(
            cart_key,
            {}
        ).get(
            "quantity",
            0
        )

        variant.remaining_stock = max(
            variant.stock - cart_quantity,
            0
        )

    context = {

        "product": product,

        "variants": variants,

    }

    return render(
        request,
        "product_detail.html",
        context
    )


# ==========================================
# PRODUCT SIZES API
# ==========================================

@api_view(["GET"])
def product_sizes(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = request.session.get("cart", {})

    variants = ProductVariant.objects.filter(
        product=product
    ).annotate(

        size_order=Case(
            When(size="XS", then=0),
            When(size="S", then=1),
            When(size="M", then=2),
            When(size="L", then=3),
            When(size="XL", then=4),
            When(size="XXL", then=5),
            output_field=IntegerField(),
        )

    ).order_by("size_order")

    data = []

    for variant in variants:

        cart_key = f"{product.id}_{variant.size}"

        cart_qty = 0

        if cart_key in cart:

            cart_qty = cart[cart_key]["quantity"]

        remaining = max(
            variant.stock - cart_qty,
            0
        )

        data.append({

            "size": variant.size,

            "stock": variant.stock,

            "remaining_stock": remaining,

        })

    return Response(data)

# ==========================================
# CONTACT
# ==========================================

def contact(request):

    if request.method == "POST":

        form = ContactMessageForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Message Sent Successfully"
            )

            return redirect("contact")

    else:

        form = ContactMessageForm()

    return render(
        request,
        "contact.html",
        {
            "form": form,
        },
    )


# ==========================================
# PRIVACY POLICY
# ==========================================

def privacy_policy(request):

    return render(
        request,
        "privacy_policy.html"
    )


# ==========================================
# SHIPPING POLICY
# ==========================================

def shipping_policy(request):

    return render(
        request,
        "shipping_policy.html"
    )


# ==========================================
# RETURN POLICY
# ==========================================

def return_policy(request):

    return render(
        request,
        "return_policy.html"
    )

def faqs(request):

    return render(
        request,
        "faqs.html"
    )

def track_order(request):

    return render(
        request,
        "track_order.html"
    )