"""Write your api app view functions here."""

from rest_framework import viewsets
from reviews.models import Review, Title, Genre
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CommentSerializer, ReviewSerializer,
    TitleSerializer, GenreSerializer
)


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
