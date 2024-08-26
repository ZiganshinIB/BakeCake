from .views import *
from django.urls import path

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', registration, name='registration'),
    path('lk/', ProfileView.as_view(), name='lk'),
    path('catalog/', CakeCatalogView.as_view(), name='catalog'),
    path('cakes/', CakesListView.as_view(), name='cakes'),
]