from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from .models import Order


# ==========================================
# MY ORDERS
# ==========================================

@never_cache
@login_required
def my_orders(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related(
            "items__product",
            "items__variant",
        )
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "my-orders.html",
        {
            "orders": orders,
        }
    )


# ==========================================
# ORDER DETAIL
# ==========================================

@never_cache
@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product",
            "items__variant",
        ),
        id=order_id,
        user=request.user,
    )

    status_steps = [
        "Pending",
        "Confirmed",
        "Packed",
        "Shipped",
        "Delivered",
    ]

    current_index = (
        status_steps.index(order.status)
        if order.status in status_steps
        else -1
    )

    return render(
        request,
        "order-detail.html",
        {
            "order": order,
            "status_steps": status_steps,
            "current_index": current_index,
        }
    )


# ==========================================
# ORDER SUCCESS
# ==========================================

@never_cache
@login_required
def order_success(request):

    order_id = request.session.get("last_order_id")

    if not order_id:

        return render(
            request,
            "order-success.html",
        )

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "order-success.html",
        {
            "order": order,
        }
    )