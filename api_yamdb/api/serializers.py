from django.db.models import Avg
from rest_framework.serializers import (
    CurrentUserDefault,
    ModelSerializer,
    SerializerMethodField,
    SlugRelatedField,
)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(ModelSerializer):
    """Сериализатор Category."""

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(ModelSerializer):
    """Сериализатор Genre."""

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(ModelSerializer):
    """Сериализатор для чтения модели Title."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        if obj.reviews.count() == 0:
            return None
        review = Review.objects.filter(title=obj).aggregate(
            rating=Avg('score')
        )
        return review['rating']


class TitleWriteSerializer(ModelSerializer):
    """Сериализатор для записи модели Title."""

    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(ModelSerializer):
    """Отзывы произведений"""

    author = SlugRelatedField(
        slug_field='username', default=CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['title']

    validators = [
        UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['title', 'author'],
            message='Нельзя оставить отзыв на одно произведение дважды',
        )
    ]


class CommentSerializer(ModelSerializer):
    """Комментарии к отзывам"""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['title']