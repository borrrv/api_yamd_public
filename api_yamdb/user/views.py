from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED)
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from api_yamdb.settings import DEFAULT_FROM_EMAIL

from .models import User
from .serializers import (RegistrationSerializer, TokenSerializer,
                          UserEditSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def registraions(request):
    """Регистрация пользователя"""

    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    email = request.POST.get('email')
    username = request.POST.get('username')
    user, username = User.objects.get_or_create(
        email=email,
        username=username
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код для получения api-tokena',
        message=f'Ваш код: {confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(user.email,),
    )
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение токена"""

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(
        User,
        username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': (str(token))}, status=HTTP_200_OK)

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """Viewset для модели User и UserSerializer."""

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=UserEditSerializer
    )
    def users_me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_401_UNAUTHORIZED)
