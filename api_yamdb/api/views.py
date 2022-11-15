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

    def perform_create(self, serializer):
        """Переопределение метода create для CommentViewSet."""

        # Доделать ##################################


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для модели Review и ReviewSerializer."""

    serializer_class = ReviewSerializer
    permission_classes = []

    def get_queryset(self):
        """Переопределение метода get_queryset для ReviewViewSet."""

        # Доделать! #############################################

    def perform_create(self, serializer):
        """Переопределение метода create для ReviewtViewSet."""

        # Доделать ##################################
