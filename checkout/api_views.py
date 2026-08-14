from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Address

from .serializers import AddressSerializer

from .services import (
    create_address,
    update_address,
    get_user_addresses,
    delete_address,
)


# ==========================================
# CREATE ADDRESS
# ==========================================

class CreateAddressAPIView(APIView):

    def post(self, request):

        serializer = AddressSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(

                serializer.errors,

                status=status.HTTP_400_BAD_REQUEST

            )

        address = create_address(

            request.user,

            serializer.validated_data

        )

        return Response(

            AddressSerializer(address).data,

            status=status.HTTP_201_CREATED

        )


# ==========================================
# UPDATE ADDRESS
# ==========================================

class UpdateAddressAPIView(APIView):

    def put(self, request, pk):

        try:

            address = Address.objects.get(

                pk=pk,

                user=request.user

            )

        except Address.DoesNotExist:

            return Response(

                {

                    "message": "Address not found."

                },

                status=status.HTTP_404_NOT_FOUND

            )

        serializer = AddressSerializer(

            address,

            data=request.data,

            partial=True

        )

        if not serializer.is_valid():

            return Response(

                serializer.errors,

                status=status.HTTP_400_BAD_REQUEST

            )

        address = update_address(

            address,

            serializer.validated_data

        )

        return Response(

            AddressSerializer(address).data,

            status=status.HTTP_200_OK

        )

# ==========================================
# LIST ADDRESSES
# ==========================================

class AddressListAPIView(APIView):

    def get(self, request):

        addresses = get_user_addresses(

            request.user

        )

        serializer = AddressSerializer(

            addresses,

            many=True

        )

        return Response(

            serializer.data,

            status=status.HTTP_200_OK

        )

# ==========================================
# DELETE ADDRESS
# ==========================================

class DeleteAddressAPIView(APIView):

    def delete(self, request, pk):

        try:

            address = Address.objects.get(

                pk=pk,

                user=request.user

            )

        except Address.DoesNotExist:

            return Response(

                {

                    "message": "Address not found."

                },

                status=status.HTTP_404_NOT_FOUND

            )

        delete_address(address)

        return Response(

            {

                "success": True

            },

            status=status.HTTP_200_OK

        )