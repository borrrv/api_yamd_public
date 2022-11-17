from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets
from reviews.models import Review, Title
from django.shortcuts import get_object_or_404
from .serializers import (
    CommentSerializer, ReviewSerializer,
    TitleSerializer, GenreSerializer
)

from reviews.models import User

from .serializer import RegistrationSerializer, TokenSerializer


@api_view(['POST'])
def registraions(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    username = serializer.validated_data['username']
    user = get_object_or_404(
        User,
        username=username
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код для получения api-tokena',
        message=f'Ваш код: {confirmation_code}',
        from_email=None,
        recipient_list=(user.email,),
    )
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
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
    

class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для модели Comment и CommentSerializer."""

    serializer_class = CommentSerializer
    permission_classes = []

    def get_queryset(self):
        """Переопределение метода get_queryset для CommentViewSet."""

        # Доделать! #############################################
        # review = get_object_or_404(Review, pk=self.kwargs.get(''))
        # return review.comments

    def perform_create(self, serializer):
        """Переопределение метода create для CommentViewSet."""

        # Доделать ##################################
        # title_id = self.kwargs.get('')
        # review_id = self.kwargs.get('')
        # review = get_object_or_404(Review, id=review_id, title=title_id)
        # serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для модели Review и ReviewSerializer."""

    serializer_class = ReviewSerializer
    permission_classes = []

    def get_queryset(self):
        """Переопределение метода get_queryset для ReviewViewSet."""

        # Доделать! #############################################
        # title = get_object_or_404(Title, pk=self.kwargs.get(''))
        # return title.reviews

    def perform_create(self, serializer):
        """Переопределение метода create для ReviewtViewSet."""

        # Доделать ##################################
        # title_id = self.kwargs.get('')
        # title = get_object_or_404(Title, id=title_id)
        # serializer.save(author=self.request.user, title=title)


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для модели Title."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category__slug',
        'genre__slug',
        'name',
        'year'
    )


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для модели Genre. Только чтение."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
