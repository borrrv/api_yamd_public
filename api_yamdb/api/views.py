"""Write your api app view functions here."""

from rest_framework import viewsets
from reviews.models import Review
from django.shortcuts import get_object_or_404
from .serializers import (CommentSerializer, ReviewSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для модели Comment и CommentSerializer."""

    serializer_class = CommentSerializer
    permission_classes = []

    def get_queryset(self):
        """Переопределение метода get_queryset для CommenViewSet."""

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
