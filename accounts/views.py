from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .services import (
    update_profile,
    change_password,
    create_address,
    update_address,
    set_default_address,
    delete_address,
    track_user_session,
)

from .models import Address, UserSession


User = get_user_model()

# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    # Already logged in
    if request.user.is_authenticated:

        return redirect(
            "profile"
        )


    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        password = request.POST.get(
            "password",
            ""
        )


        # ------------------------------------------
        # VALIDATION
        # ------------------------------------------

        if not email or not password:

            messages.error(
                request,
                "Please enter your email and password."
            )

            return render(
                request,
                "accounts/login.html",
                {
                    "email": email,
                }
            )


        # ------------------------------------------
        # AUTHENTICATE
        # ------------------------------------------

        user = authenticate(
            request,
            username=email,
            password=password
        )


        # ------------------------------------------
        # INVALID LOGIN
        # ------------------------------------------

        if user is None:

            messages.error(
                request,
                "Invalid email or password."
            )

            return render(
                request,
                "accounts/login.html",
                {
                    "email": email,
                }
            )


        # ------------------------------------------
        # INACTIVE ACCOUNT
        # ------------------------------------------

        if not user.is_active:

            messages.error(
                request,
                "This account has been disabled."
            )

            return render(
                request,
                "accounts/login.html",
                {
                    "email": email,
                }
            )


        # ------------------------------------------
        # DJANGO SESSION LOGIN
        # ------------------------------------------

        login(
            request,
            user
        )


        # ------------------------------------------
        # TRACK LOGIN SESSION
        # ------------------------------------------

        track_user_session(
            request,
            user
        )


        # ------------------------------------------
        # SUCCESS MESSAGE
        # ------------------------------------------

        messages.success(
            request,
            f"Welcome back, {user.first_name or 'there'}!"
        )


        # ------------------------------------------
        # REDIRECT TO REQUESTED PAGE
        # ------------------------------------------

        # If Django sent the customer to login
        # from another protected page,
        # send them back there.

        next_url = request.GET.get(
            "next"
        )

        if next_url:

            return redirect(
                next_url
            )


        # ------------------------------------------
        # DEFAULT REDIRECT
        # ------------------------------------------

        return redirect(
            "profile"
        )


    # ------------------------------------------
    # GET REQUEST
    # ------------------------------------------

    return render(
        request,
        "accounts/login.html"
    )
# ==========================================
# REGISTER
# ==========================================

def register_view(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        phone_number = request.POST.get(
            "phone_number",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        form_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
        }

        # ------------------------------------------
        # REQUIRED FIELDS
        # ------------------------------------------

        if not first_name or not email or not password:

            messages.error(
                request,
                "Please fill in all required fields."
            )

            return render(
                request,
                "accounts/register.html",
                {
                    "form_data": form_data,
                }
            )

        # ------------------------------------------
        # PASSWORD MATCH
        # ------------------------------------------

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "accounts/register.html",
                {
                    "form_data": form_data,
                }
            )

        # ------------------------------------------
        # PASSWORD LENGTH
        # ------------------------------------------

        if len(password) < 8:

            messages.error(
                request,
                "Password must be at least 8 characters long."
            )

            return render(
                request,
                "accounts/register.html",
                {
                    "form_data": form_data,
                }
            )

        # ------------------------------------------
        # EMAIL EXISTS
        # ------------------------------------------

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "An account with this email already exists."
            )

            return render(
                request,
                "accounts/register.html",
                {
                    "form_data": form_data,
                }
            )

        # ------------------------------------------
        # PHONE EXISTS
        # ------------------------------------------

        if (
            phone_number
            and User.objects.filter(
                phone_number=phone_number
            ).exists()
        ):

            messages.error(
                request,
                "An account with this phone number already exists."
            )

            return render(
                request,
                "accounts/register.html",
                {
                    "form_data": form_data,
                }
            )

        # ------------------------------------------
        # CREATE UNIQUE USERNAME
        # ------------------------------------------

        username_base = email.split("@")[0]

        username = username_base

        counter = 1

        while User.objects.filter(
            username=username
        ).exists():

            username = f"{username_base}{counter}"

            counter += 1

        # ------------------------------------------
        # CREATE USER
        # ------------------------------------------

        try:

            user = User.objects.create_user(

                username=username,

                email=email,

                password=password,

                first_name=first_name,

                last_name=last_name,

                phone_number=(
                    phone_number
                    if phone_number
                    else None
                ),

            )

        except IntegrityError:

            messages.error(
                request,
                "We couldn't create your account. Please try again."
            )

            return render(
                request,
                "accounts/register.html",
                {
                    "form_data": form_data,
                }
            )

        # ------------------------------------------
        # LOGIN AFTER REGISTER
        # ------------------------------------------

        login(request, user)

        messages.success(
            request,
            "Welcome to Shruja Couture. Your account has been created!"
        )

        return redirect("profile")

    return render(
        request,
        "accounts/register.html"
    )


# ==========================================
# PROFILE
# ==========================================

@login_required(login_url="login")
def profile_view(request):

    user = request.user

    # ==========================================
    # HANDLE PROFILE FORM
    # ==========================================

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "update_profile":


            first_name = request.POST.get(
                "first_name",
                ""
            ).strip()

            last_name = request.POST.get(
                "last_name",
                ""
            ).strip()

            phone_number = request.POST.get(
                "phone_number",
                ""
            ).strip()

            date_of_birth = request.POST.get(
                "date_of_birth",
                ""
            ).strip()

            gender = request.POST.get(
                "gender",
                ""
            ).strip()

            # ------------------------------------------
            # FIRST NAME REQUIRED
            # ------------------------------------------

            if not first_name:

                messages.error(
                    request,
                    "First name is required."
                )

                return redirect("profile")

            # ------------------------------------------
            # PHONE NUMBER DUPLICATE CHECK
            # ------------------------------------------

            if phone_number:

                phone_exists = User.objects.filter(
                    phone_number=phone_number
                ).exclude(
                    id=user.id
                ).exists()

                if phone_exists:

                    messages.error(
                        request,
                        "This phone number is already linked to another account."
                    )

                    return redirect("profile")

            # ------------------------------------------
            # GENDER VALIDATION
            # ------------------------------------------

            valid_genders = [
                choice[0]
                for choice in User.Gender.choices
            ]

            if gender and gender not in valid_genders:

                messages.error(
                    request,
                    "Please select a valid gender."
                )

                return redirect("profile")

            # ------------------------------------------
            # PREPARE PROFILE DATA
            # ------------------------------------------

            profile_data = {
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": (
                    phone_number
                    if phone_number
                    else None
                ),
                "gender": gender,
            }

            # ------------------------------------------
            # DATE OF BIRTH
            # ------------------------------------------

            if date_of_birth:

                from datetime import datetime

                try:

                    parsed_date_of_birth = datetime.strptime(
                        date_of_birth,
                        "%Y-%m-%d"
                    ).date()

                except ValueError:

                    messages.error(
                        request,
                        "Please enter a valid date of birth."
                    )

                    return redirect("profile")

            else:

                parsed_date_of_birth = None


            profile_data[
                "date_of_birth"
            ] = parsed_date_of_birth


            # ------------------------------------------
            # PROFILE IMAGE
            # ------------------------------------------

            remove_profile_image = (
                request.POST.get(
                    "remove_profile_image",
                    "false"
                ).lower() == "true"
            )

            # REMOVE EXISTING PROFILE IMAGE

            if remove_profile_image:

                if user.profile_image:

                    user.profile_image.delete(
                        save=False
                    )

                user.profile_image = None

            # UPLOAD / CHANGE PROFILE IMAGE

            elif request.FILES.get("profile_image"):

                uploaded_image = request.FILES[
                    "profile_image"
                ]

                allowed_content_types = {
                    "image/jpeg",
                    "image/png",
                    "image/webp",
                }

                if uploaded_image.content_type not in allowed_content_types:

                    messages.error(
                        request,
                        "Please choose a JPG, PNG or WEBP image."
                    )

                    return redirect("profile")

                if uploaded_image.size > 5 * 1024 * 1024:

                    messages.error(
                        request,
                        "Please choose an image smaller than 5 MB."
                    )

                    return redirect("profile")

                if user.profile_image:

                    user.profile_image.delete(
                        save=False
                    )

                user.profile_image = uploaded_image

            # ------------------------------------------
            # UPDATE USING SERVICE
            # ------------------------------------------

            update_profile(
                user,
                profile_data
            )

            messages.success(
                request,
                "Your profile has been updated successfully."
            )

            return redirect("profile")

        # ==========================================
        # CHANGE PASSWORD
        # ==========================================
        elif action == "change_password":

            current_password = request.POST.get(
                "current_password",
                ""
            )

            new_password = request.POST.get(
                "new_password",
                ""
            )

            confirm_password = request.POST.get(
                "confirm_password",
                ""
            )


            # ------------------------------------------
            # CHANGE USING SERVICE
            # ------------------------------------------

            try:

                change_password(
                    user,
                    current_password,
                    new_password,
                    confirm_password
                )


            except ValidationError as error:

                for message in error.messages:

                    messages.error(
                        request,
                        message,
                        extra_tags="password_error"
                    )


                return redirect(
                    "profile"
                )


            # ------------------------------------------
            # KEEP USER LOGGED IN
            # ------------------------------------------

            update_session_auth_hash(
                request,
                user
            )


            # ------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------

            messages.success(
                request,
                "Your password has been changed successfully.",
                extra_tags="password_success"
            )


            return redirect(
                "profile"
            )
        

            

            


           


            


        # ==========================================
        # ADD ADDRESS
        # ==========================================

        elif action == "add_address":

            full_name = request.POST.get(
                "full_name",
                ""
            ).strip()

            phone_number = request.POST.get(
                "address_phone_number",
                ""
            ).strip()

            address_line_1 = request.POST.get(
                "address_line_1",
                ""
            ).strip()

            address_line_2 = request.POST.get(
                "address_line_2",
                ""
            ).strip()

            city = request.POST.get(
                "city",
                ""
            ).strip()

            state = request.POST.get(
                "state",
                ""
            ).strip()

            postal_code = request.POST.get(
                "postal_code",
                ""
            ).strip()

            country = request.POST.get(
                "country",
                "India"
            ).strip()

            address_type = request.POST.get(
                "address_type",
                Address.AddressType.HOME
            ).strip()

            is_default = (
                request.POST.get("is_default") == "true"
            )

            # ------------------------------------------
            # REQUIRED FIELDS
            # ------------------------------------------

            if (
                not full_name
                or not phone_number
                or not address_line_1
                or not city
                or not state
                or not postal_code
                or not country
            ):

                messages.error(
                    request,
                    "Please fill in all required address fields."
                )

                return redirect("profile")

            # ------------------------------------------
            # PIN CODE VALIDATION
            # ------------------------------------------

            if (
                not postal_code.isdigit()
                or len(postal_code) != 6
            ):

                messages.error(
                    request,
                    "Please enter a valid 6-digit PIN code."
                )

                return redirect("profile")

            # ------------------------------------------
            # ADDRESS TYPE VALIDATION
            # ------------------------------------------

            valid_address_types = [
                choice[0]
                for choice in Address.AddressType.choices
            ]

            if address_type not in valid_address_types:

                address_type = Address.AddressType.HOME

            # ------------------------------------------
            # CREATE USING SERVICE
            # ------------------------------------------

            address_data = {
                "full_name": full_name,
                "phone_number": phone_number,
                "address_line_1": address_line_1,
                "address_line_2": address_line_2,
                "city": city,
                "state": state,
                "postal_code": postal_code,
                "country": country,
                "address_type": address_type,
                "is_default": is_default,
            }

            create_address(
                user,
                address_data
            )

            messages.success(
                request,
                "Your address has been saved successfully."
            )

            return redirect("profile")


        # ==========================================
        # UPDATE ADDRESS
        # ==========================================

        elif action == "update_address":

            address_id = request.POST.get(
                "address_id",
                ""
            ).strip()

            try:

                address = Address.objects.get(
                    id=address_id,
                    user=user
                )

            except (
                Address.DoesNotExist,
                ValueError
            ):

                messages.error(
                    request,
                    "We couldn't find that address."
                )

                return redirect(
                    "profile"
                )


            full_name = request.POST.get(
                "full_name",
                ""
            ).strip()

            phone_number = request.POST.get(
                "address_phone_number",
                ""
            ).strip()

            address_line_1 = request.POST.get(
                "address_line_1",
                ""
            ).strip()

            address_line_2 = request.POST.get(
                "address_line_2",
                ""
            ).strip()

            city = request.POST.get(
                "city",
                ""
            ).strip()

            state = request.POST.get(
                "state",
                ""
            ).strip()

            postal_code = request.POST.get(
                "postal_code",
                ""
            ).strip()

            country = request.POST.get(
                "country",
                "India"
            ).strip()

            address_type = request.POST.get(
                "address_type",
                Address.AddressType.HOME
            ).strip()

            is_default = (
                request.POST.get(
                    "is_default"
                ) == "true"
            )


            # ------------------------------------------
            # REQUIRED FIELDS
            # ------------------------------------------

            if (
                not full_name
                or not phone_number
                or not address_line_1
                or not city
                or not state
                or not postal_code
                or not country
            ):

                messages.error(
                    request,
                    "Please fill in all required address fields."
                )

                return redirect(
                    "profile"
                )


            # ------------------------------------------
            # PIN CODE VALIDATION
            # ------------------------------------------

            if (
                not postal_code.isdigit()
                or len(postal_code) != 6
            ):

                messages.error(
                    request,
                    "Please enter a valid 6-digit PIN code."
                )

                return redirect(
                    "profile"
                )


            # ------------------------------------------
            # ADDRESS TYPE VALIDATION
            # ------------------------------------------

            valid_address_types = [
                choice[0]
                for choice
                in Address.AddressType.choices
            ]

            if (
                address_type
                not in valid_address_types
            ):

                address_type = (
                    Address.AddressType.HOME
                )


            # Keep the current default address as default
            # unless another address is explicitly made default.
            if address.is_default:

                is_default = True


            # ------------------------------------------
            # UPDATE USING SERVICE
            # ------------------------------------------

            address_data = {
                "full_name": full_name,
                "phone_number": phone_number,
                "address_line_1": address_line_1,
                "address_line_2": address_line_2,
                "city": city,
                "state": state,
                "postal_code": postal_code,
                "country": country,
                "address_type": address_type,
                "is_default": is_default,
            }

            update_address(
                address,
                address_data
            )


            messages.success(
                request,
                "Your address has been updated successfully."
            )


            return redirect(
                "profile"
            )


        # ==========================================
        # REMOVE ADDRESS
        # ==========================================

        elif action == "remove_address":

            address_id = request.POST.get(
                "address_id",
                ""
            ).strip()


            # ------------------------------------------
            # FIND ADDRESS
            # ------------------------------------------

            try:

                address = Address.objects.get(
                    id=address_id,
                    user=user
                )

            except (
                Address.DoesNotExist,
                ValueError
            ):

                messages.error(
                    request,
                    "We couldn't find that address."
                )

                return redirect(
                    "profile"
                )


            # ------------------------------------------
            # DELETE USING SERVICE
            # ------------------------------------------

            delete_address(
                address
            )


            # ------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------

            messages.success(
                request,
                "Your address has been removed."
            )


            return redirect(
                "profile"
            )


        # ==========================================
        # SET DEFAULT ADDRESS
        # ==========================================

        elif action == "set_default_address":

            address_id = request.POST.get(
                "address_id",
                ""
            ).strip()


            # ------------------------------------------
            # FIND ADDRESS
            # ------------------------------------------

            try:

                address = Address.objects.get(
                    id=address_id,
                    user=user
                )

            except (
                Address.DoesNotExist,
                ValueError
            ):

                messages.error(
                    request,
                    "We couldn't find that address."
                )

                return redirect(
                    "profile"
                )


            # ------------------------------------------
            # ALREADY DEFAULT
            # ------------------------------------------

            if address.is_default:

                messages.info(
                    request,
                    "This is already your default address."
                )

                return redirect(
                    "profile"
                )


            # ------------------------------------------
            # SET DEFAULT USING SERVICE
            # ------------------------------------------

            set_default_address(
                address
            )


            # ------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------

            messages.success(
                request,
                "Your default address has been updated."
            )


            return redirect(
                "profile"
            )
       
        # ==========================================
    # SAVED ADDRESSES
    # ==========================================

    addresses = Address.objects.filter(
        user=user
    ).order_by(
        "-is_default",
        "-created_at"
    )
    

    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        "addresses":
            addresses,

    }


    return render(
        request,
        "accounts/profile.html",
        context
    )


# ==========================================
# LOGOUT
# ==========================================

@login_required(login_url="login")
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("products:home")