from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from users.models import User
from reviews.validators import validate_year


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
        return self.name[:settings.NUMBER_OF_SOMETHING_VERY_IMPORTANT]


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
