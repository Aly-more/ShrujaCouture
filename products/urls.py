from django.urls import path
from . import views

app_name = "products"


urlpatterns = [

    # ==========================================
    # HOME
    # ==========================================

    path(
        "",
        views.home,
        name="home"
    ),


    # ==========================================
    # SHOP
    # ==========================================

    path(
        "shop/",
        views.shop,
        name="shop"
    ),


    # ==========================================
    # NEW ARRIVALS
    # ==========================================

    path(
        "new-arrivals/",
        views.new_arrivals,
        name="new_arrivals"
    ),


    # ==========================================
    # CATEGORY
    # ==========================================

    path(
        "category/<int:category_id>/",
        views.category_products,
        name="category_products"
    ),


    # ==========================================
    # PRODUCT DETAIL
    # ==========================================

    path(
        "product/<slug:slug>/",
        views.product_detail,
        name="product_detail"
    ),

    # ==========================================
    # FAQS
    # ==========================================

    path(
        "faqs/",
        views.faqs,
        name="faqs"
    ),

    # ==========================================
    # TRACK-ORDER
    # ==========================================

    path(
        "track-order/",
        views.track_order,
        name="track_order"
    ),

    # ==========================================
    # PRODUCT SIZE API
    # ==========================================

    path(
        "api/product/<int:product_id>/sizes/",
        views.product_sizes,
        name="product_sizes"
    ),

    path("contact/", 
         views.contact, 
         name="contact"),

    path(
            "privacy-policy/",
            views.privacy_policy,
            name="privacy_policy"
        ),

    path(
            "shipping-policy/",
            views.shipping_policy,
            name="shipping_policy"
        ),

    path(
            "return-policy/",
            views.return_policy,
            name="return_policy"
        ),

]