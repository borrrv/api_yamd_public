from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, IntegerField

from user.models import User


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(max_length=20, verbose_name='название жанра')
    slug = models.SlugField(unique=True, verbose_name='ссылка')

    class Meta:
        """Meta настройки модели Genre."""

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        """Метод str модели Genre."""
        return self.name


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Ссылка'
    )

    class Meta:
        """Meta настройки модели Category."""
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        """Метод str модели Category."""
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(verbose_name='Год выпуска')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        """Meta настройки модели Title."""

        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_name_year'
            )
        ]

    def __str__(self):
        """Метод str модели Title."""
        return self.name

    @property
    def rating(self):
        """Метод для расчета рейтинга произведения."""
        return self.reviews.aggregate(
            Avg('score', output_field=IntegerField()))['score__avg']


class GenreTitle(models.Model):
    """Модель произведение-жанр."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        related_name='genre',
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст Отзыва')
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Рейтинг выставляется по 10 бальной шкале.'),
            MaxValueValidator(10, 'Рейтинг выставляется по 10 бальной шкале.')
        ])
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True)

    class Meta:
        """Meta модели Reviews.
           Содержит сортировку,ограничения и verbose_names."""

        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author_title')
        ]


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментарии'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')

    class Meta:
        """Meta модели Comment.
           Содержит сортировку и verbose_names."""

        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
