from reviews.models import Comment, Review, Title, Genre, User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email', 'username',)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('__all__')


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

        fields = ('title', 'author', 'text', 'score', 'pub_date')
        model = Review
        validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['title', 'author'],
            message='Отзыв уже написан.'
        )]


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title."""

    genre = serializers.SlugRelatedField(slug_field='slug',
                                         many=True,
                                         queryset=Genre.objects.all())

    class Meta:
        fields = ('name', 'year', 'category', 'genre')
        model = Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    pass


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    pass
