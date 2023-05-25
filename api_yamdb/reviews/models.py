from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from datetime import datetime as dt


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Slug категории', unique=True)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Genre(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Slug жанра', unique=True)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256,)
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[MaxValueValidator(dt.now().year)],
    )
    description = models.TextField(verbose_name='Описание',)
    genre = models.ManyToManyField(Genre, verbose_name='Slug жанра',)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, verbose_name='Slug категории',
        blank=True, null=True,
    )

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Review(models.Model):
    title = models.OneToOneField(
        Title, on_delete=models.CASCADE, verbose_name='ID произведения',
        related_name='reviews',
    )
    text = models.TextField(verbose_name='Текст отзыва',)
    score = models.IntegerField(
        verbose_name='Оценка',
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review")
        ]

    def __str__(self):
        return f'{self.title} ({self.pk})'


class Comment(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='ID произведения',
        related_name='comments',
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='ID отзыва',
        related_name='comments',
    )
    text = models.TextField(verbose_name='Текст комментария',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        related_name='Дата комментария',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.title} ({self.pk})'
