from rest_framework import serializers
from .models import User


# 🔹 For user registration (input only)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# 🔹 For returning user info (no password)
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# 🔹 For login/signup responses (user + tokens)
class TokenResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user = UserResponseSerializer()
    tokens = serializers.DictField()


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


