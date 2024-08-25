from django.urls import include, path

from .api_views import CakeViewSet, CakeLevelViewSet, CakeShapeViewSet, CakeToppingViewSet, CakeBerryViewSet, \
    CakeDecorViewSet, OrderViewSet, CalculateCakePriceApiView, CakeApiView

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
    path('calc/', CalculateCakePriceApiView.as_view()),
    path('cake/', CakeApiView.as_view())
]