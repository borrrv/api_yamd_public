from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    def username_validate(self, value):
        username = value.lower()
        if value == 'me':
            raise serializers.ValidationError(f'Недопустимо имя {username}')
        return value

    class Meta:
        model = User
        fields = ("username", "email")


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'bio',
                  'role', 'email')


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio',
                  'role', 'email')
        model = User
        read_only_fields = ('role',)
