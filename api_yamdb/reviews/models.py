from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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
        through='TitleGenre',
        db_index=True,
        verbose_name='Жанр',
        help_text='Укажите жанр',
    )
    year = models.IntegerField(
        db_index=True,
        verbose_name='Дата выхода',
        help_text='Укажите дату выхода',
        validators=(validate_year,)
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
    """Модель категорий."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Необходимо названия котегории'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:10]


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Необходимо названия жанра',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:10]


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Необходимо произведение',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
        help_text='Необходим жанр',
    )

    def __str__(self) -> str:
        return f'{self.title},{self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10, 'Максимальная оценка - 10'),
            MinValueValidator(1, 'Минимальная оценка - 1')
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_review'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Комментарий к отзыву"
        verbose_name_plural = "Комментарии к отзыву"

    def __str__(self):
        return self.text[:10]
