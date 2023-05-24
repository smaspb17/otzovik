from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(prefix='title', viewset='TitleViewSet', basename='title')
router_v1.register(prefix='category', viewset='CategoryViewSet', basename='category')
router_v1.register(prefix='genre', viewset='GenreViewSet', basename='genre')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
