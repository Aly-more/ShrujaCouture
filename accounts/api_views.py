from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Address
from django.shortcuts import get_object_or_404

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ProfileSerializer,
    AddressSerializer,
    LogoutSerializer,
)

from .services import (
    register_user,
    login_user,
    logout_user,
    update_profile,
    create_address,
    update_address,
    set_default_address,
)



class RegisterAPIView(APIView):

    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def get(self, request):

        serializer = RegisterSerializer()

        return Response(serializer.data)

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = register_user(serializer.validated_data)

            return Response(
                {
                    "success": True,
                    "message": "Account created successfully.",
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            result = login_user(
                serializer.validated_data["user"]
            )

            user = result["user"]

            return Response(

                {
                    "success": True,
                    "message": "Login successful.",

                    "access": result["access"],

                    "refresh": result["refresh"],

                    "user": {

                        "id": user.id,

                        "first_name": user.first_name,

                        "last_name": user.last_name,

                        "email": user.email,

                    }

                },

                status=status.HTTP_200_OK

            )

        return Response(

            {

                "success": False,

                "errors": serializer.errors,

            },

            status=status.HTTP_400_BAD_REQUEST

        )
    
class CurrentUserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(

            {

                "success": True,

                "user": serializer.data,

            },

            status=status.HTTP_200_OK,

        )
    
class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ProfileSerializer(request.user)

        return Response(

            {

                "success": True,

                "profile": serializer.data,

            },

            status=status.HTTP_200_OK

        )

    def put(self, request):

        serializer = ProfileSerializer(

            request.user,

            data=request.data

        )

        if serializer.is_valid():

            user = update_profile(

                request.user,

                serializer.validated_data

            )

            return Response(

                {

                    "success": True,

                    "message": "Profile updated successfully.",

                    "profile": ProfileSerializer(user).data,

                },

                status=status.HTTP_200_OK

            )

        return Response(

            {

                "success": False,

                "errors": serializer.errors,

            },

            status=status.HTTP_400_BAD_REQUEST

        )

    def patch(self, request):

        serializer = ProfileSerializer(

            request.user,

            data=request.data,

            partial=True

        )

        if serializer.is_valid():

            user = update_profile(

                request.user,

                serializer.validated_data

            )

            return Response(

                {

                    "success": True,

                    "message": "Profile updated successfully.",

                    "profile": ProfileSerializer(user).data,

                },

                status=status.HTTP_200_OK

            )

        return Response(

            {

                "success": False,

                "errors": serializer.errors,

            },

            status=status.HTTP_400_BAD_REQUEST

        )
    

class AddressListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        addresses = Address.objects.filter(
            user=request.user
        ).order_by("-is_default", "-id")

        serializer = AddressSerializer(
            addresses,
            many=True
        )

        return Response(

            {
                "success": True,
                "addresses": serializer.data,
            },

            status=status.HTTP_200_OK,

        )

    def post(self, request):

        serializer = AddressSerializer(
            data=request.data
        )

        if serializer.is_valid():

            address = create_address(
                request.user,
                serializer.validated_data
            )

            return Response(

                {
                    "success": True,
                    "message": "Address added successfully.",
                    "address": AddressSerializer(address).data,
                },

                status=status.HTTP_201_CREATED,

            )

        return Response(

            {
                "success": False,
                "errors": serializer.errors,
            },

            status=status.HTTP_400_BAD_REQUEST,

        )
    

class AddressDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):

        return get_object_or_404(
            Address,
            id=pk,
            user=request.user,
    )

    def get(self, request, pk):

        address = self.get_object(request, pk)

        serializer = AddressSerializer(address)

        return Response(

            {
                "success": True,
                "address": serializer.data,
            },

            status=status.HTTP_200_OK,

        )

    def put(self, request, pk):

        address = self.get_object(request, pk)

        serializer = AddressSerializer(
            address,
            data=request.data
        )

        if serializer.is_valid():

            address = update_address(
                address,
                serializer.validated_data
            )

            return Response(

                {
                    "success": True,
                    "message": "Address updated successfully.",
                    "address": AddressSerializer(address).data,
                },

                status=status.HTTP_200_OK,

            )

        return Response(

            {
                "success": False,
                "errors": serializer.errors,
            },

            status=status.HTTP_400_BAD_REQUEST,

        )

    def patch(self, request, pk):

        address = self.get_object(request, pk)

        serializer = AddressSerializer(
            address,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            address = update_address(
                address,
                serializer.validated_data
            )

            return Response(

                {
                    "success": True,
                    "message": "Address updated successfully.",
                    "address": AddressSerializer(address).data,
                },

                status=status.HTTP_200_OK,

            )

        return Response(

            {
                "success": False,
                "errors": serializer.errors,
            },

            status=status.HTTP_400_BAD_REQUEST,

        )

    def delete(self, request, pk):

        address = self.get_object(request, pk)

        address.delete()

        return Response(

            {
                "success": True,
                "message": "Address deleted successfully.",
            },

            status=status.HTTP_204_NO_CONTENT,

    )


class DefaultAddressAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        address = get_object_or_404(
            Address,
            id=pk,
            user=request.user,
        )

        address = set_default_address(address)

        return Response(

            {
                "success": True,
                "message": "Default address updated successfully.",
                "address": AddressSerializer(address).data,
            },

            status=status.HTTP_200_OK,

        )
    

class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():

            success = logout_user(
                serializer.validated_data["refresh"]
            )

            if success:

                return Response(

                    {
                        "success": True,
                        "message": "Logged out successfully.",
                    },

                    status=status.HTTP_200_OK,

                )

            return Response(

                {
                    "success": False,
                    "message": "Invalid refresh token.",
                },

                status=status.HTTP_400_BAD_REQUEST,

            )

        return Response(

            {
                "success": False,
                "errors": serializer.errors,
            },

            status=status.HTTP_400_BAD_REQUEST,

        )