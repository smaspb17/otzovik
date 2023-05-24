from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
