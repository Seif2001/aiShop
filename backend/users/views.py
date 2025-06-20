import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import hashlib

from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserResponseSerializer,
    TokenResponseSerializer
)
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes



# 🔹 Signup Endpoint
@extend_schema(
    request=UserSerializer,
    responses={
        201: TokenResponseSerializer,
        400: str,
    },
    summary="User signup endpoint",
    description="Creates a new user account and returns JWT tokens."
)
@api_view(['POST'])
@permission_classes([AllowAny])

def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return Response({
        "message": "Login successful",
        "user": UserResponseSerializer(user).data,
        "tokens": token_data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 🔹 Login Endpoint
@extend_schema(
    request=UserLoginSerializer,
    responses={
        200: TokenResponseSerializer,
        401: str,
        404: str,
    },
    summary="User login endpoint",
    description="Authenticates user and returns JWT tokens."
)

@api_view(['POST'])
@permission_classes([AllowAny])
@extend_schema(
    request=UserLoginSerializer,
    responses={
        200: TokenResponseSerializer,
        401: str,
        404: str,
    },
    summary="User login endpoint",
    description="Authenticates user and returns JWT tokens."
)
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)

    token_data = {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

    return Response({
    "message": "Login successful",
    "user": UserResponseSerializer(user).data,
    "tokens": token_data
    }, status=status.HTTP_200_OK)




# 🔹 Get All Users (optional - for admin/demo)
@extend_schema(
    summary="Get all users",
    responses={200: UserResponseSerializer(many=True)},
    description="Returns a list of all users."
)
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserResponseSerializer(users, many=True)
    return Response(serializer.data)


# 🔹 Get, Update, or Delete a User by ID
@extend_schema(
    summary="Get, update, or delete a user by ID",
    request=UserSerializer,
    responses={
        200: UserResponseSerializer,
        400: str,
        404: str,
    },
    description="GET retrieves a user by ID, PUT updates a user, DELETE removes a user."
)
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserResponseSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(UserResponseSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
