from rest_framework.serializers import (ModelSerializer, SlugRelatedField, CurrentUserDefault,
                                        ValidationError,) 

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

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            author = self.context['request'].user
            if author.reviews.filter(title_id=title_id).exists():
                raise ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return data

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise ValidationError(
                'Оценка в диапазоне от 1 до 10 включительно'
            )
        return value


class CommentSerializer(ModelSerializer):
    """Комментарии к отзывам"""

    author = SlugRelatedField(slug_field='username',
                              read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['title']
