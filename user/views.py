
from authorization.models import CustomUser
from exceptions.custom_apiexception_class import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.views import APIView
from utils.custom_response import custom_response
from django.shortcuts import get_object_or_404
from utils.custom_permission import IsStaff
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from .serializers import UserProfileSerializer

load_dotenv()
User = get_user_model()


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    csrf_protect_method = method_decorator(csrf_protect)

    @swagger_auto_schema(
        operation_description="Retrieve your personal profile.",
        responses={
            200: openapi.Response(
                description="user profile is returned. Must be authenticated",
                schema=UserProfileSerializer()
            ),
            404: openapi.Response(
                description="User item not found."
            ),
        },
    )
    def get(self, request):
        email = request.user.email

        try:
            profile = CustomUser.objects.get(email__exact=email)
        except CustomUser.DoesNotExist:
            raise CustomAPIException(
                detail="User profile not found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()

        serializer = UserProfileSerializer(profile)
        return custom_response(status_code=status.HTTP_200_OK, message="Success.", data=serializer.data)


class AllUsersView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]
    csrf_protect_method = method_decorator(csrf_protect)

    @csrf_protect_method
    @swagger_auto_schema(
        operation_description="Retrieve all users. Available for users with is_staf permission",
        responses={
            200: openapi.Response(
                description="Successfully retrieved all users items.",
                schema=UserProfileSerializer(many=True)
            ),
            500: openapi.Response(
                description="Internal server error, custom error message."
            ),
        }
    )
    def get(self, request):
        try:
            users = CustomUser.objects.all()
            serializer = UserProfileSerializer(users, many=True)
            return custom_response(status_code=status.HTTP_200_OK, message="Success", data=serializer.data)
        except CustomUser.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="No users found.")
        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]
    csrf_protect_method = method_decorator(csrf_protect)

    @csrf_protect_method
    @swagger_auto_schema(
        operation_description="Retrieve a specific user by its UUID. Available for users with is_staf permission",
        responses={
            200: openapi.Response(
                description="A single user is returned.",
                schema=UserProfileSerializer()
            ),
            404: openapi.Response(
                description="User item not found."
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'id',
                in_=openapi.IN_PATH,
                description="UUID of the user to retrieve.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID
            ),
        ]
    )
    def get(self, request, pk):
        try:
            user = get_object_or_404(CustomUser, pk=pk)
            serializer = UserProfileSerializer(user)
            return custom_response(status_code=status.HTTP_200_OK, message="Success", data=serializer.data)
        except CustomUser.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="User not found")
        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
