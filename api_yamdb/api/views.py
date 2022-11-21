from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED)
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets, mixins
from .serializers import (RegistrationSerializer, TokenSerializer,
                          CommentSerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializer,
                          UserEditSerializer, UserSerializer,
                          CategorySerializer, TitleListSerializer)
from .permissions import (IsAdmin, AdminOrReadOnly,
                          IsAdminOrModeratorOrOwnerOrReadOnly)
from reviews.models import User, Review, Title, Genre, Category
from .filters import TitleFilter


@api_view(['POST'])
@permission_classes([AllowAny])
def registraions(request):
    """Регистрация пользователя"""
    user = request.user
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
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


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для модели Comment и CommentSerializer."""

    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrModeratorOrOwnerOrReadOnly]

    def get_queryset(self):
        """Переопределение метода get_queryset для CommentViewSet."""

        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Переопределение метода create для CommentViewSet."""

        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для модели Review и ReviewSerializer."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrModeratorOrOwnerOrReadOnly]

    def get_queryset(self):
        """Переопределение метода get_queryset для ReviewViewSet."""

        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Переопределение метода create для ReviewtViewSet."""

        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для модели Title."""

    queryset = (Title.objects.all().annotate(_rating=Avg('reviews__score'))
                .order_by('name'))
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleSerializer


class ListReadCreateDestroy(mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Базовый viewset для GET, POST, DELETE."""
    pass


class GenreViewSet(ListReadCreateDestroy):
    """Viewset для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('name',)


class CategoriesViewSet(ListReadCreateDestroy):
    """Viewset для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
