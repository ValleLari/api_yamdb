from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

from reviews.validators import validate_year


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


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название',
        help_text='Необходимо названия произведения',
    )
    category = models.ForeignKey(
        'Category',
        related_name='titles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        db_index=True,
        verbose_name='Категория',
        help_text='Укажите категорию',
    )
    genre = models.ManyToManyField(
        'Genre',
        db_index=True,
        verbose_name='Жанр',
        help_text='Укажите жанр',
    )
    year = models.IntegerField(
        db_index=True,
        verbose_name='Дата выхода',
        help_text='Укажите дату выхода',
        validators=(validate_year,),
    )
    description = models.TextField(
        max_length=200,
        null=True,
        verbose_name='Описание',
        help_text='Необходимо описание',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:10]


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=settings.BIG_INT_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=settings.SMALL_INT_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.BIG_INT_LENGTH,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=settings.SMALL_INT_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Отзыв', help_text='Текст отзыва')
    score = models.IntegerField(
        verbose_name='Оценка',
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review_title"
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Комментарий', help_text='Текст комментария'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
