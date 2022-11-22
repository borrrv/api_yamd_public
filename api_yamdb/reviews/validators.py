from rest_framework import serializers


def username_validate(value):
    """Валидатор недопустимого usernmae - me."""
    if value == 'me':
        raise serializers.ValidationError(f"Недопустимо имя '{value}'")
    return value
