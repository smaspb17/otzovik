from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    prefix='title', viewset=views.TitleViewSet, basename='title',
)
router_v1.register(
    prefix='category', viewset=views.CategoryViewSet, basename='category',
)
router_v1.register(
    prefix='genre', viewset=views.GenreViewSet, basename='genre',
)
router_v1.register(
    prefix='review', viewset=views.ReviewViewSet, basename='review',
)
router_v1.register(
    prefix='comment', viewset=views.CommentViewSet, basename='comment',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
