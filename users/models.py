from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
)
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = ((USER, 'User'), (ADMIN, 'Moderator'), (MODERATOR, 'Admin'))
    email = models.EmailField(
        blank=False, max_length=settings.BIG_INT_LENGTH, unique=True
    )
    bio = models.TextField(
        max_length=settings.VERY_BIG_INT_LENGTH,
        null=True,
        blank=True,
        verbose_name='О себе',
    )
    role = models.TextField(blank=True, choices=ROLES, default=USER)
    username = models.CharField(
        max_length=settings.MID_SMALL_INT_LENGTH,
        verbose_name='Имя пользователя',
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимый символ',
            )
        ],
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=settings.MID_SMALL_INT_LENGTH,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=settings.MID_SMALL_INT_LENGTH,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
