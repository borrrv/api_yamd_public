from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации."""

    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    def validate_username(self, value):
        """Проверка на запрещенный username - me."""

        username = value.lower()
        if username == 'me':
            raise serializers.ValidationError(f"Недопустимо имя '{username}'")
        return value

    class Meta:
        model = User
        fields = ("username", "email")


class TokenSerializer(serializers.Serializer):
    """Сериалайзер для токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""

    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        """Meta настройки сериалайзера для модели User."""

        model = User
        fields = ('first_name', 'last_name',
                  'username', 'bio',
                  'role', 'email')


class UserEditSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""

    class Meta:
        """Meta настройки UserEditSerializer для модели User."""

        fields = ('first_name', 'last_name',
                  'username', 'bio',
                  'role', 'email')
        model = User
        read_only_fields = ('role',)
