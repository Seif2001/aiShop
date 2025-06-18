# from drf_spectacular.utils import extend_schema
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import User
# from .serializers import UserSerializer
# from django.contrib.auth.hashers import check_password
# from rest_framework_simplejwt.tokens import RefreshToken



# @extend_schema(
#     summary="Get all users or create a new user",
#     request=UserSerializer,
#     responses=UserSerializer,
#     description="GET returns all users; POST creates a new user with name and email."
# )

# @api_view(['GET', 'POST'])
# def user_list(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

# @extend_schema(
#     summary="Get all user or update or delete a single user all requiring user ID",
#     request=UserSerializer,
#     responses=UserSerializer,
#     description="GET retrieves a user by ID; PUT updates a user by ID; DELETE removes a user by ID."
# ) 


# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @extend_schema(
#     request=UserSerializer,
#     responses=UserSerializer,
#     summary="User login endpoint",
#     description="login user account and returns JWT tokens."
# )
# @api_view(['POST'])
# def login(request):
#     email = request.data.get("email")
#     password = request.data.get("password")

#     try:
#         user = User.objects.get(email=email)
#         if not check_password(password, user.password):
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#     except User.DoesNotExist:
#         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#     refresh = RefreshToken.for_user(user)
#     token_data = {
#         "refresh": str(refresh),
#         "access": str(refresh.access_token)
#     }

#     user_data = UserSerializer(user).data
#     user_data.pop("password", None)

#     return Response({
#         "message": "Login successful",
#         "user": user_data,
#         "tokens": token_data
#     }, status=200)
    
# @extend_schema(
#     request=UserSerializer,
#     responses=UserSerializer,
#     summary="User signup endpoint",
#     description="Creates a new user account and returns JWT tokens."
# )


# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()

#         refresh = RefreshToken.for_user(user)
#         token_data = {
#             "refresh": str(refresh),
#             "access": str(refresh.access_token)
#         }

#         user_data = serializer.data
#         user_data.pop("password", None)

#         return Response({
#             "message": "Signup successful",
#             "user": user_data,
#             "tokens": token_data
#         }, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserResponseSerializer,
    TokenResponseSerializer
)
from django.contrib.auth.hashers import check_password
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

        user_data = UserResponseSerializer(user).data

        return Response({
            "message": "Signup successful",
            "user": user_data,
            "tokens": token_data
        }, status=status.HTTP_201_CREATED)

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
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
        if not check_password(password, user.password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    refresh = RefreshToken.for_user(user)
    token_data = {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

    user_data = UserResponseSerializer(user).data

    return Response({
        "message": "Login successful",
        "user": user_data,
        "tokens": token_data
    }, status=200)


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
