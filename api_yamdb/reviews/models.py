from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from datetime import datetime as dt


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug категории', unique=True)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug жанра', unique=True)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Title(models.Model):
    name = models.CharField('Название', max_length=256,)
    year = models.PositiveIntegerField(
        'Год выпуска', validators=[MaxValueValidator(dt.now().year)],)
    description = models.TextField('Описание',)
    genre = models.ManyToManyField(Genres, verbose_name='Slug жанра',)
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, verbose_name='Slug категории',
        blank=True, null=True,
    )

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Review(models.Model):
    title = models.OneToOneField(
        'Title', on_delete=models.CASCADE, verbose_name='ID произведения',
        related_name='reviews',
    )
    text = models.TextField('Текст отзыва',)
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    def __str__(self):
        return f'{self.title} ({self.pk})'
      

class Comment(models.Model):
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, verbose_name='ID произведения',
        related_name='comments',
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='ID отзыва',
        related_name='comments',
    )
    text = models.TextField('Текст комментария',)

    def __str__(self):
        return f'{self.title} ({self.pk})'


