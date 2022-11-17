from rest_framework import serializers
from reviews.models import Comment, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        """Meta настройки сериалайзера для модели Comment."""

        fields = ('review', 'author', 'text', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Review."""

    title = serializers.SlugRelatedField(
        slug_field='title',
        read_only=True,
    )

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Meta настройки сериалайзера для модели Review."""

        fields = ('title', 'author', 'text', 'rating', 'pub_date')
        model = Review


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title."""

    genre = serializers.ChoiceField()
    class Meta:
        fields = ('name', 'year', 'category', 'genre')
        model = Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    pass


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    pass
