from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from user_agents import parse

from rest_framework_simplejwt.tokens import (
    RefreshToken,
    TokenError,
)

from .models import (
    Address,
    UserSession,
)


User = get_user_model()


# =====================================================
# REGISTER USER
# =====================================================

@transaction.atomic
def register_user(validated_data):

    validated_data.pop(
        "confirm_password"
    )

    password = validated_data.pop(
        "password"
    )

    # Normalize email
    validated_data["email"] = (
        validated_data["email"]
        .strip()
        .lower()
    )

    username = (
        validated_data["email"]
        .split("@")[0]
    )

    base_username = username
    counter = 1


    while User.objects.filter(
        username=username
    ).exists():

        username = (
            f"{base_username}{counter}"
        )

        counter += 1


    validated_data["username"] = (
        username
    )


    user = User.objects.create(
        **validated_data
    )

    user.set_password(
        password
    )

    user.save()


    return user


# =====================================================
# LOGIN USER
# =====================================================

def login_user(user):
    """
    Generate JWT tokens for the authenticated user.
    """

    refresh = RefreshToken.for_user(
        user
    )


    return {

        "access":
            str(refresh.access_token),

        "refresh":
            str(refresh),

        "user":
            user,

    }


# =====================================================
# LOGOUT USER
# =====================================================

def logout_user(refresh_token):
    """
    Blacklist the refresh token.
    """

    try:

        token = RefreshToken(
            refresh_token
        )

        token.blacklist()

        return True


    except TokenError:

        return False


# =====================================================
# UPDATE PROFILE
# =====================================================

@transaction.atomic
def update_profile(
    user,
    validated_data
):
    """
    Update the authenticated user's profile.
    """

    for field, value in (
        validated_data.items()
    ):

        setattr(
            user,
            field,
            value
        )


    user.save()


    return user


# =====================================================
# CREATE ADDRESS
# =====================================================

@transaction.atomic
def create_address(
    user,
    validated_data
):
    """
    Create a new address for the authenticated user.

    The first address automatically becomes
    the default address.
    """

    has_addresses = (
        Address.objects.filter(
            user=user
        ).exists()
    )


    # First address must be default
    if not has_addresses:

        validated_data[
            "is_default"
        ] = True


    # If this address should be default,
    # remove default status from existing addresses.
    if validated_data.get(
        "is_default",
        False
    ):

        Address.objects.filter(
            user=user,
            is_default=True
        ).update(
            is_default=False
        )


    address = Address.objects.create(
        user=user,
        **validated_data
    )


    return address


# =====================================================
# UPDATE ADDRESS
# =====================================================

@transaction.atomic
def update_address(
    address,
    validated_data
):
    """
    Update an existing address.
    """

    if validated_data.get(
        "is_default",
        False
    ):

        Address.objects.filter(
            user=address.user,
            is_default=True
        ).exclude(
            id=address.id
        ).update(
            is_default=False
        )


    for field, value in (
        validated_data.items()
    ):

        setattr(
            address,
            field,
            value
        )


    address.save()


    return address


# =====================================================
# SET DEFAULT ADDRESS
# =====================================================

@transaction.atomic
def set_default_address(
    address
):
    """
    Make the selected address the user's
    default address.
    """

    # Nothing to change
    if address.is_default:

        return address


    Address.objects.filter(
        user=address.user,
        is_default=True
    ).update(
        is_default=False
    )


    address.is_default = True

    address.save(
        update_fields=[
            "is_default"
        ]
    )


    return address


# =====================================================
# DELETE ADDRESS
# =====================================================

@transaction.atomic
def delete_address(
    address
):
    """
    Delete an address.

    If the deleted address was the default,
    automatically promote another saved address
    to default.
    """

    user = address.user

    was_default = (
        address.is_default
    )


    address.delete()


    # If a non-default address was deleted,
    # there is nothing else to do.
    if not was_default:

        return


    # Pick another saved address.
    next_address = (
        Address.objects
        .filter(
            user=user
        )
        .order_by(
            "-created_at"
        )
        .first()
    )


    if next_address:

        next_address.is_default = True

        next_address.save(
            update_fields=[
                "is_default"
            ]
        )

# =====================================================
# CHANGE PASSWORD
# =====================================================

@transaction.atomic
def change_password(
    user,
    current_password,
    new_password,
    confirm_password
):
    """
    Validate and change the authenticated user's password.
    """

    # ------------------------------------------
    # REQUIRED FIELDS
    # ------------------------------------------

    if (
        not current_password
        or not new_password
        or not confirm_password
    ):

        raise ValidationError(
            "Please fill in all password fields."
        )


    # ------------------------------------------
    # VERIFY CURRENT PASSWORD
    # ------------------------------------------

    if not user.check_password(
        current_password
    ):

        raise ValidationError(
            "Your current password is incorrect."
        )


    # ------------------------------------------
    # PASSWORDS MUST MATCH
    # ------------------------------------------

    if new_password != confirm_password:

        raise ValidationError(
            "The new passwords do not match."
        )


    # ------------------------------------------
    # PREVENT REUSING CURRENT PASSWORD
    # ------------------------------------------

    if user.check_password(
        new_password
    ):

        raise ValidationError(
            "Your new password must be different from your current password."
        )


    # ------------------------------------------
    # DJANGO PASSWORD VALIDATION
    # ------------------------------------------

    validate_password(
        new_password,
        user=user
    )


    # ------------------------------------------
    # CHANGE PASSWORD
    # ------------------------------------------

    user.set_password(
        new_password
    )

    user.save(
        update_fields=[
            "password"
        ]
    )


    return user

# =====================================================
# TRACK USER SESSION
# =====================================================

@transaction.atomic
def track_user_session(
    request,
    user
):
    """
    Create or update the authenticated user's
    current login session.
    """

    # ------------------------------------------
    # ENSURE SESSION EXISTS
    # ------------------------------------------

    if not request.session.session_key:

        request.session.save()


    session_key = (
        request.session.session_key
    )


    # ------------------------------------------
    # USER AGENT
    # ------------------------------------------

    user_agent_string = (
        request.META.get(
            "HTTP_USER_AGENT",
            ""
        )
    )

    user_agent = parse(
        user_agent_string
    )


    # ------------------------------------------
    # BROWSER
    # ------------------------------------------

    browser = (
        user_agent.browser.family
        or "Unknown Browser"
    )


    # ------------------------------------------
    # OPERATING SYSTEM
    # ------------------------------------------

    operating_system = (
        user_agent.os.family
        or "Unknown OS"
    )


    # ------------------------------------------
    # DEVICE TYPE
    # ------------------------------------------

    if user_agent.is_mobile:

        device = "Mobile"

    elif user_agent.is_tablet:

        device = "Tablet"

    elif user_agent.is_pc:

        device = "Desktop"

    else:

        device = "Other"


    # ------------------------------------------
    # IP ADDRESS
    # ------------------------------------------

    ip_address = (
        request.META.get(
            "REMOTE_ADDR"
        )
    )


    # ------------------------------------------
    # CREATE / UPDATE SESSION
    # ------------------------------------------

    user_session, created = (
        UserSession.objects.update_or_create(

            session_key=session_key,

            defaults={

                "user":
                    user,

                "ip_address":
                    ip_address,

                "browser":
                    browser,

                "operating_system":
                    operating_system,

                "device":
                    device,

            },

        )
    )


    return user_session