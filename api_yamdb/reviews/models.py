from datetime import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models


class Categories(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveIntegerField(
        'Год выпуска', validators=[MaxValueValidator(dt.now().year)])
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genres,)
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name
