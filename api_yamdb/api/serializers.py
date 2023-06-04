from django.db.models import Avg
from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    EmailField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    SlugRelatedField,
    ValidationError
)
from rest_framework.validators import (
    UniqueTogetherValidator,
    UniqueValidator,
)
from .validators import validate_username
from reviews.models import Category, Comment, Genre, Review, Title, User


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


class SignUpSerializer(Serializer):
    username = CharField(
        required=True,
        max_length=150,
        validators=[validate_username, ]
    )
    email = EmailField(required=True, max_length=254)

    def validate(self, data):
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if (User.objects.filter(username=data['username']).exists()
                or User.objects.filter(email=data['email']).exists()):
            raise ValidationError(
                'Пользователь с такими данными уже существует!'
            )
        return data


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


class FromContext(object):
    requires_context = True

    def __init__(self, value_fn):
        self.value_fn = value_fn

    def __call__(self, serializer_field):
        self.value = self.value_fn(serializer_field.context)
        return self.value


class ReviewSerializer(ModelSerializer):
    """Отзывы произведений"""
    author = SlugRelatedField(
        slug_field='username', default=CurrentUserDefault(), read_only=True
    )
    title = SlugRelatedField(
        slug_field='name',
        read_only=True,
        default=FromContext(
            lambda context: context.get('view').kwargs['title_id']
        )
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['title']
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author'],
            )
        ]


class CommentSerializer(ModelSerializer):
    """Комментарии к отзывам"""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class EmailVerificationSerializer(ModelSerializer):
    token = CharField(max_length=555)

    class Meta:
        model = User
        fields = ('token',)


class UserSerializer(ModelSerializer):
    username = CharField(
        required=True,
        max_length=150,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserMeSerializer(ModelSerializer):
    username = CharField(
        required=True,
        max_length=150,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class TokenSerializer(Serializer):
    username = CharField(
        required=True,
        max_length=150,
        validators=[validate_username, ]
    )
    confirmation_code = CharField(required=True)
