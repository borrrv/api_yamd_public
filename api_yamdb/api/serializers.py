import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.SlugRelatedField(slug_field='text',
                                          read_only=True)

    class Meta:
        """Meta настройки сериалайзера для модели Comment."""

        fields = ('review', 'author', 'text', 'pub_date', 'id')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Review."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        """Валидация для сериализатора Review."""

        if self.context['request'].method != 'POST':
            return data

        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)

        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Вы не можете добавлять несколько '
                                  'отзывов на произведение')
        return data

    class Meta:
        """Meta настройки сериалайзера для модели Review."""

        fields = ('author', 'text', 'score', 'pub_date', 'id')
        model = Review


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        """Meta настройки сериалайзера для модели Title."""

        fields = ('id', 'name', 'year', 'category',
                  'genre', 'description', 'rating')
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year')
            )
        ]

    def validate_year(self, value):
        """Валидация года для TitleSerializer."""
        year = dt.date.today().year

        if year < value:
            raise serializers.ValidationError('Проверьте год!')

        return value

    def get_rating(self, obj):
        """Вызов метода для подсчета рейтинга."""
        return obj.rating


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        """Meta настройки сериалайзера для модели Genre."""

        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        """Meta настройки сериалайзера для модели Category."""

        fields = ('name', 'slug')
        model = Category


class TitleListSerializer(serializers.ModelSerializer):
    """Serializer для модели Title для отображения списком."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj) -> int:
        """Вызов метода для подсчета рейтинга."""
        return obj.rating

    class Meta:
        """Meta настройки сериалайзера списка для модели Title."""

        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
