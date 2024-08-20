from django.urls import include, path

from .api_views import CakeViewSet, CakeLevelViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

router = SimpleRouter()
router.register(r'cakes', CakeViewSet)
router.register(r'cakelevels', CakeLevelViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('', include(router.urls)),
]