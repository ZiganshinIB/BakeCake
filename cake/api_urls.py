from django.urls import include, path

from .api_views import CakeViewSet, CakeLevelViewSet, CakeShapeViewSet, CakeToppingViewSet, CakeBerryViewSet, \
    CakeDecorViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

router = SimpleRouter()
router.register(r'cakes', CakeViewSet)
router.register(r'cakelevels', CakeLevelViewSet)
router.register(r'cakeshape', CakeShapeViewSet)
router.register(r'caketopping', CakeToppingViewSet)
router.register(r'cakeberry', CakeBerryViewSet)
router.register(r'cakedecor', CakeDecorViewSet)

router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('', include(router.urls)),
]