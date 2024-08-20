from oauthlib.uri_validate import query
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from django.db.models import Q

from .models import Cake, CakeLevel
from .serializers import CakeSerializer, CakeLevelSerializer
from .permissions import IsOwnerOrReadOnly, CanUpdateCake, CanDeleteCake


class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.filter(is_published=True)
    serializer_class = CakeSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsOwnerOrReadOnly(), CanUpdateCake()]
        elif self.action == 'destroy':
            return [CanDeleteCake]
        else:
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        level = self.request.query_params.get('level', None)
        shape = self.request.query_params.get('shape', None)
        topping = self.request.query_params.get('topping', None)
        berry = self.request.query_params.get('berry', None)
        decor = self.request.query_params.get('decor', None)
        filters = Q()
        if level is not None:
            filters &= Q(level__level_count=level)
        if shape is not None:
            filters &= Q(shape__shape=shape)
        if topping is not None:
            filters &= Q(topping__cake_topping=topping)
        if berry is not None:
            filters &= Q(berry__cake_berry=berry)
        if decor is not None:
            filters &= Q(decor__cake_decor=decor)
        if filters:
            self.queryset = self.queryset.filter(filters)
        return self.queryset


class CakeLevelViewSet(viewsets.ModelViewSet):
    queryset = CakeLevel.objects.all()
    serializer_class = CakeLevelSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsOwnerOrReadOnly(), CanUpdateCakeLevel()]
        elif self.action == 'destroy':
            return [CanDeleteCake]
        else:
            return [permissions.IsAuthenticated()]