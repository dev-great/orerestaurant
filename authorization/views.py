from django.shortcuts import get_object_or_404
from authorization.models import CustomUser
from exceptions.custom_apiexception_class import *
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.views import APIView
from utils.custom_response import custom_response
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from .serializers import ChangePasswordSerializer, UserSerializer, TokenObtainPairResponseSerializer, TokenRefreshResponseSerializer, TokenVerifyResponseSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


load_dotenv()
User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={status.HTTP_201_CREATED: UserSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return custom_response(status_code=status.HTTP_201_CREATED, message="Success", data=response_data)
        else:
            error_msg = str(serializer.errors)
            return CustomAPIException(detail=str(serializer.errors), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class LoginView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid credentials.",
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return CustomAPIException(
                detail="Invalid token.", status_code=status.HTTP_401_UNAUTHORIZED).get_full_details()
        except Exception as e:
            return CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()

        return custom_response(status_code=status.HTTP_200_OK, message="Success", data=serializer.validated_data)


class TokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid token.",
        }
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return custom_response(status_code=status.HTTP_200_OK, message="Token is refresh.", data=response.data)
        else:
            return CustomAPIException(detail="Token is invalid.", status_code=response.status_code, data=response.data).get_full_details()


class TokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid token.",
        }
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return custom_response(status_code=status.HTTP_200_OK, message="Token is valid.", data=response.data)
        else:
            return CustomAPIException(detail="Token is invalid or expired.", status_code=response.status_code, data=response.data).get_full_details()


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'refresh', openapi.IN_QUERY, description="Refresh token", type=openapi.TYPE_STRING, required=True
            )
        ],
        responses={
            status.HTTP_205_RESET_CONTENT: "Logout successful.",
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid credentials.",
        }
    )
    def post(self, request):

        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return custom_response(status_code=status.HTTP_205_RESET_CONTENT, message="Logout successful.", data=None)

        except Exception as e:
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_description="Change the password for the currently authenticated user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='The current password of the user.'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='The new password for the user.')
            }
        ),
        responses={
            200: openapi.Response(
                description="Password updated successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='No additional data')
                    }
                )
            ),
            400: openapi.Response(
                description="Invalid credentials or bad request.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='Error details')
                    }
                )
            )
        }
    )
    def put(self, request, *args, **kwargs):

        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return custom_response(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Invalid Credential",
                    data={"old_password": ["Wrong password."]}
                )

            # Set new password
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return custom_response(status_code=status.HTTP_200_OK, message='Password updated successfully', data=None)

        return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message=str(serializer.errors))


class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        user_email = self.request.user.email
        return get_object_or_404(CustomUser, email=user_email)

    @swagger_auto_schema(
        operation_description="Delete the account of the currently authenticated user.",
        responses={
            200: openapi.Response(
                description="User account successfully deleted.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='HTTP status code'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='No additional data')
                    }
                )
            ),
            404: openapi.Response(
                description="User not found."
            ),
            500: openapi.Response(
                description="Internal server error."
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            user_email = request.user.email

            paysita_user = self.get_object()
            self.perform_destroy(paysita_user)

            return custom_response(status_code=status.HTTP_200_OK, message="User deleted", data=None)
        except CustomUser.DoesNotExist:
            return CustomAPIException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

    def perform_destroy(self, instance):
        instance.delete()
