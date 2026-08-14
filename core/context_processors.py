from wishlist.models import Wishlist
from core.models import InstagramPost


def cart_count(request):

    # ==========================================
    # CART COUNT
    # ==========================================

    cart = request.session.get("cart", {})

    cart_count = sum(

        item["quantity"]

        for item in cart.values()

    )

    # ==========================================
    # WISHLIST
    # ==========================================

    if request.user.is_authenticated:

        wishlist = Wishlist.objects.filter(
            user=request.user
        )

    else:

        if not request.session.session_key:
            request.session.create()

        wishlist = Wishlist.objects.filter(
            session_key=request.session.session_key
        )

    wishlist_count = wishlist.count()

    wishlist_ids = list(

        wishlist.values_list(
            "product_id",
            flat=True
        )

    )

    # ==========================================
    # SITE INFORMATION
    # ==========================================

    site_info = {

        "instagram": "https://www.instagram.com/shrujacouture/",

        "facebook": "https://www.facebook.com/share/1CyA886JMX/",

        "whatsapp": "https://wa.me/8355856436?text=Hi%20Shruja%20Couture!%20I%20have%20a%20question.",

        "email": "Shrujacouture@gmail.com",

        "phone": "+91 83558 56436",

        "address": "Worli, Mumbai-18 , Maharashtra",

    }

    # ==========================================
# INSTAGRAM JOURNAL
# ==========================================

    instagram_posts = InstagramPost.objects.filter(
            is_active=True
        )

    return {

        "cart_count": cart_count,

        "wishlist_count": wishlist_count,

        "wishlist_ids": wishlist_ids,

        "SITE_INFO": site_info,

        "instagram_posts": instagram_posts,

    }