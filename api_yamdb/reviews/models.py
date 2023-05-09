from django.db import models
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
