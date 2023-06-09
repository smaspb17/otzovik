from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    SlugField,
    TextChoices,
    TextField,
    UniqueConstraint,
)

from api.validators import current_year_validator


class User(AbstractUser):
    class Role(TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMINISTRATOR = 'admin'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    bio = TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    email = EmailField(
        verbose_name='Эл. почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    is_verified = BooleanField(default=False)
    role = CharField(
        verbose_name='Роль',
        max_length=30,
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.Role.ADMINISTRATOR

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR


class Category(Model):
    name = CharField(verbose_name='Название', max_length=256)
    slug = SlugField(verbose_name='Slug категории', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Genre(Model):
    name = CharField(verbose_name='Название', max_length=256)
    slug = SlugField(verbose_name='Slug жанра', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Title(Model):
    name = CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True,
    )
    year = PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[current_year_validator],
        db_index=True,
    )
    description = TextField(
        verbose_name='Описание',
    )
    genre = ManyToManyField(
        to=Genre,
        verbose_name='Slug жанра',
        db_index=True,
    )
    category = ForeignKey(
        to=Category,
        on_delete=SET_NULL,
        verbose_name='Slug категории',
        blank=True,
        null=True,
        related_name='titles',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Review(Model):
    title = ForeignKey(
        to=Title,
        on_delete=CASCADE,
        related_name='reviews',
        verbose_name='ID произведения',
    )
    text = TextField(
        verbose_name='Текст отзыва',
    )
    score = PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    author = ForeignKey(to=User, on_delete=CASCADE, related_name='reviews')
    pub_date = DateTimeField(
        verbose_name='Дата отзыва', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            UniqueConstraint(fields=['author', 'title'], name='unique_review')
        ]

    def __str__(self):
        return self.text[:10]


class Comment(Model):
    review = ForeignKey(
        to=Review,
        on_delete=CASCADE,
        verbose_name='ID отзыва',
        related_name='comments',
    )
    text = TextField(
        verbose_name='Текст комментария',
    )
    author = ForeignKey(to=User, on_delete=CASCADE, related_name='comments')
    pub_date = DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
