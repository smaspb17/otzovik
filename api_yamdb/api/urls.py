from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                       ReviewViewSet, CommentViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    prefix='title', viewset=TitleViewSet, basename='title',
)
router_v1.register(
    prefix='category', viewset=CategoryViewSet, basename='category',
)
router_v1.register(
    prefix='genre', viewset=GenreViewSet, basename='genre',
)
router_v1.register(
    prefix=r'title/(?P<title_id>[\d]+)/review',
    viewset=ReviewViewSet,
    basename='review'
)
router_v1.register(
    prefix=r'title/(?P<title_id>[\d]+)/review/(?P<review_id>[\d]+)/comment',
    viewset=CommentViewSet,
    basename='comment',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
