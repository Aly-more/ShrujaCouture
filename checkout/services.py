from accounts.models import Address


# ==========================================
# CREATE ADDRESS
# ==========================================

def create_address(user, validated_data):

    if validated_data.get("is_default"):

        Address.objects.filter(
            user=user,
            is_default=True,
        ).update(
            is_default=False
        )

    address = Address.objects.create(

        user=user,

        **validated_data

    )

    return address


# ==========================================
# UPDATE ADDRESS
# ==========================================

def update_address(address, validated_data):

    if validated_data.get("is_default"):

        Address.objects.filter(

            user=address.user,

            is_default=True

        ).exclude(

            id=address.id

        ).update(

            is_default=False

        )

    for field, value in validated_data.items():

        setattr(

            address,

            field,

            value

        )

    address.save()

    return address

# ==========================================
# GET USER ADDRESSES
# ==========================================

def get_user_addresses(user):

    return Address.objects.filter(

        user=user

    ).order_by(

        "-is_default",

        "-created_at"

    )

# ==========================================
# DELETE ADDRESS
# ==========================================

def delete_address(address):

    user = address.user

    was_default = address.is_default

    address.delete()

    if was_default:

        next_address = Address.objects.filter(

            user=user

        ).order_by(

            "-created_at"

        ).first()

        if next_address:

            next_address.is_default = True

            next_address.save(
                update_fields=["is_default"]
            )