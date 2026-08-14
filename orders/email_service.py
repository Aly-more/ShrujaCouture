from django.core.mail import send_mail
from django.conf import settings


# ==========================================
# ORDER CONFIRMATION EMAIL
# ==========================================

def send_order_confirmation_email(order):

    subject = f"Order Confirmed - {order.order_number}"

    message = f"""
Hi {order.customer_name},

Thank you for shopping with Shruja Couture.

Order Number:
{order.order_number}

Order Total:
₹{order.total}

Payment Status:
{order.payment_status}

We have received your order and will begin processing it shortly.

Love,
Shruja Couture
"""

    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )


# ==========================================
# SHIPMENT EMAIL
# ==========================================

def send_shipped_email(order):

    subject = f"Your Order Has Been Shipped - {order.order_number}"

    message = f"""
Hi {order.customer_name},

Good news!

Your order has been shipped.

Order Number:
{order.order_number}

We will notify you once it is delivered.

Love,
Shruja Couture
"""

    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )

def send_delivered_email(order):

    subject = f"Order Delivered - {order.order_number}"

    message = f"""
Hi {order.customer_name},

Great news!

Your order has been delivered successfully.

Order Number:
{order.order_number}

We hope you love your purchase.

Thank you for shopping with Shruja Couture.

We look forward to serving you again.

Love,
Shruja Couture
"""

    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )


# ==========================================
# DELIVERED EMAIL
# ==========================================

def send_delivered_email(order):

    subject = f"Order Delivered - {order.order_number}"

    message = f"""
Hi {order.customer_name},

Your order has been successfully delivered.

Order Number:
{order.order_number}

We hope you love your purchase.

Thank you for shopping with Shruja Couture.

Love,
Shruja Couture
"""

    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )

