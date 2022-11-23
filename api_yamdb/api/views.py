from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .permissions import AdminOrReadOnly, IsAdminOrModeratorOrOwnerOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleListSerializer, TitleSerializer)


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
        """Переопределение класса сериализатора для методов retrieve, list."""
        if self.action in ('retrieve', 'list'):
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
