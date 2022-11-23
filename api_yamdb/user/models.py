from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(unique=True, blank=False, max_length=254)
    role = models.CharField(
        choices=ROLES,
        default=USER,
        max_length=10,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=100,
        null=True,
        unique=True
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        """Сортировка и проверка на уникальность username и email."""

        ordering = ['username']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        """Метод str модели User."""
        return self.username
