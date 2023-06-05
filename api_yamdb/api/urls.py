from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    SignUpView,
    VerifyEmailView,
    UserViewSet,
    # UsersViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    prefix='titles',
    viewset=TitleViewSet,
    basename='titles',
)
router_v1.register(
    prefix='categories',
    viewset=CategoryViewSet,
    basename='categories',
)
router_v1.register(
    prefix='genres',
    viewset=GenreViewSet,
    basename='genres',
)
router_v1.register(
    prefix=r'titles/(?P<title_id>[\d]+)/reviews',
    viewset=ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    prefix=r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    viewset=CommentViewSet,
    basename='comments',
)
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(route='v1/', view=include(router_v1.urls)),
    path(route='v1/auth/signup/', view=SignUpView.as_view()),
    path(route='v1/auth/token/', view=VerifyEmailView.as_view()),
]
