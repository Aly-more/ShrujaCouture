from rest_framework import serializers

from accounts.models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:

        model = Address

        fields = [
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
        ]