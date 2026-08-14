from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from accounts.models import Address
from cart.utils import calculate_cart_totals


@login_required
def checkout(request):

    cart = request.session.get("cart", {})

    totals = calculate_cart_totals(cart)

    addresses = Address.objects.filter(
        user=request.user
    ).order_by("-is_default", "-id")

    context = {

        "cart": cart,

        "addresses": addresses,

        **totals,

    }

    # ==========================================
    # DEBUG
    # ==========================================

    print("\n" + "=" * 60)
    print("CHECKOUT PAGE")
    print("Session Key :", request.session.session_key)
    print("Session Cart:", request.session.get("cart"))
    print("=" * 60 + "\n")

    return render(
        request,
        "checkout.html",
        context,
    )



@login_required
def order_success(request):

    return render(
        request,
        "order_success.html"
    )

# ==========================================
# ADDRESS LIST PARTIAL
# ==========================================

def address_list_partial(request):

    addresses = Address.objects.filter(

        user=request.user

    ).order_by(

        "-is_default",

        "-created_at"

    )

    html = render_to_string(

        "includes/address_list.html",

        {

            "addresses": addresses,

        },

        request=request,

    )

    return JsonResponse(

        {

            "html": html

        }

    )