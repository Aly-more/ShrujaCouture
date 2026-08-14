from django.urls import path

from .api_views import (
    RegisterAPIView,
    LoginAPIView,
    CurrentUserAPIView,
    ProfileAPIView,
    AddressListCreateAPIView,
    AddressDetailAPIView,
    DefaultAddressAPIView,
    LogoutAPIView,
)

app_name = "accounts_api"

urlpatterns = [

    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
        "me/",
        CurrentUserAPIView.as_view(),
        name="current-user",
    ),

    path(
    "logout/",
    LogoutAPIView.as_view(),
    name="logout",
    ),

    path(
    "profile/",
    ProfileAPIView.as_view(),
    name="profile",
    ),

    path(
    "addresses/",
        AddressListCreateAPIView.as_view(),
        name="address-list-create",
    ),

    path(
        "addresses/<int:pk>/",
            AddressDetailAPIView.as_view(),
            name="address-detail",
    ),

    path(
        "addresses/<int:pk>/default/",
            DefaultAddressAPIView.as_view(),
            name="default-address",
    ),


]