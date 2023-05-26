from rest_framework.serializers import (ModelSerializer, SlugRelatedField, CurrentUserDefault,
                                        ValidationError,)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review


class ReviewSerializer(ModelSerializer):
    """Отзывы произведений"""
    author = SlugRelatedField(
        slug_field='username',
        default=CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['title']

    validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author'],
                message='Нельзя оставить отзыв на одно произведение дважды'
            )
        ]   
   

class CommentSerializer(ModelSerializer):
    """Комментарии к отзывам"""

    author = SlugRelatedField(slug_field='username',
                              read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['title']
