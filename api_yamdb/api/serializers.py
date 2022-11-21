import datetime as dt
from django.shortcuts import get_object_or_404
from reviews.models import Comment, Review, Title, Genre, User, Category, GenreTitle
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    def validate_username(self, value):
        username = value.lower()
        if username == 'me':
            raise serializers.ValidationError(f"Недопустимо имя '{username}'")
        return value

    class Meta:
        model = User
        fields = ("username", "email")


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
        fields = ('first_name', 'last_name',
                  'username', 'bio',
                  'role', 'email')


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio',
                  'role', 'email')
        model = User
        read_only_fields = ('role',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.SlugRelatedField(slug_field='text',
                                          read_only=True)

    class Meta:
        """Meta настройки сериалайзера для модели Comment."""

        fields = ('review', 'author', 'text', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Review."""

    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
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

    genres = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'category',
                  'genres', 'description')
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year')
            )
        ]

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError('Проверьте год!')
        return value


class TitleListSerializer(serializers.ModelSerializer):
    """Serializer для модели Title для отображения списком."""

    class Meta:
        fields = ('id', 'name')
        model = Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category

    '''
    def validate_slug(self, value):
        if re.fullmatch(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError('Поле slug должно сотоять из букв и цифр!')
        return value
    '''