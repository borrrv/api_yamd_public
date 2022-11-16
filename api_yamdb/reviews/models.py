"""Create your models here."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)


class Title(models.Model):
   """Модель произведений."""
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category',
        verbose_name = 'категория'
    )
    genres = models.ForeignKey(
        Genre,
        null=True,
        blank=True,
        related_name='genres',
        verbose_name = 'жанры'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель произведение-жанр."""
    pass


class Review(models.Model):
    """Модель отзывов."""

    title = models.IntegerField(verbose_name='Отзыв')
    # title = models.ForeignKey(
    #     Title,
    #     on_delete=models.CASCADE,
    #     related_name='reviews',
    #     verbose_name='Отзыв'
    # )
    author = models.CharField(verbose_name='Автор')
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='reviews',
    #     verbose_name='Автор'
    # )
    text = models.TextField(verbose_name='Текст Отзыва')
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Рейтинг выставляется по 10 бальной шкале.'),
            MaxValueValidator(10, 'Рейтинг выставляется по 10 бальной шкале.')
        ])
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

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
    author = models.CharField(verbose_name='Автор')
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='comments',
    #     verbose_name='Автор'
    # )
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
