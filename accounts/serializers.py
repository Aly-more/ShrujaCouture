from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Address


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "confirm_password",
        )

    def validate_email(self, value):

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return value.lower()

    def validate_phone_number(self, value):

        if value:

            if User.objects.filter(phone_number=value).exists():
                raise serializers.ValidationError(
                    "Phone number already exists."
                )

        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        return attrs


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        email = attrs.get("email").lower()
        password = attrs.get("password")

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account has been disabled."
            )

        attrs["user"] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile_image",
            "date_of_birth",
            "gender",
            "is_email_verified",
        )


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile_image",
            "date_of_birth",
            "gender",
        )

        read_only_fields = (
            "email",
        )


class AddressSerializer(serializers.ModelSerializer):

    class Meta:

        model = Address

        fields = (
            "id",
            "full_name",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "address_type",
            "is_default",
        )

        read_only_fields = (
            "id",
        )


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()