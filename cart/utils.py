def calculate_cart_totals(cart):

    subtotal = sum(
        item["price"] * item["quantity"]
        for item in cart.values()
    )

    shipping = 0 if subtotal >= 1999 else 99

    total = subtotal + shipping

    return {
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    }