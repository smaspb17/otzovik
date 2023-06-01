from os import linesep

import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .permissions import (
    IsAdmin,
    IsAuthorOrReadOnly,
    IsModerator,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    EmailVerificationSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer,
)
from .utils import Util


class CreateListDestroyViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    """Общий класс для CategoryViewSet и GenreViewSet."""

    pass


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = ()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdmin | IsModerator | IsAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(model=Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(model=Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdmin | IsModerator | IsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            model=Review, id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            model=Review, id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data

        # getting tokens
        user_email = User.objects.get(email=user['email'])
        tokens = RefreshToken.for_user(user_email).access_token
        # send email for user verification
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = f'http://{current_site}{relative_link}?token={str(tokens)}'
        email_body = (
            f'Привет, {user["username"]}{linesep}'
            'Перейди по ссылке ниже, '
            f'чтобы подтвердить свою электронную почту{linesep}'
            f'{absurl}'
        )
        data = {
            'email_body': email_body,
            'to_email': user['email'],
            'email_subject': 'Verify your email',
        }

        Util.send_email(data=data)

        return Response(
            data={'user_data': user, 'access_token': str(tokens)},
            status=HTTP_201_CREATED,
        )


class VerifyEmailView(GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {'email': 'Successfully activated'}, status=HTTP_200_OK
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {'error': 'Activation Expired'}, status=HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {'error': 'Invalid token'}, status=HTTP_400_BAD_REQUEST
            )


class UserViewSet(ViewSet):
    pass


class UsersViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
