from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'Admin'
    MODERATOR = 'Moderator'
    USER = 'User'
    ROLES = [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    ]
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=ROLES,
        default=USER,
        max_length=10,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=100,
        null=True,
        unique=True,
    )

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
