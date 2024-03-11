from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    """
    переопределение сериалайзера, который использует djoser для создания пользователя из за того,
    что у нас имеются нестандартные поля
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']


class CurrentUserSerializer(serializers.ModelSerializer):
    """
    cериалайзер для работы с текущим пользователем
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'image', 'password')
