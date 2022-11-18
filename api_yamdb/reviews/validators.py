from rest_framework import serializers


def username_validate(value):
    if value == 'me':
        raise serializers.ValidationError(f'Недопустимо имя {value}')
    return value
