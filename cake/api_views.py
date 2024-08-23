from oauthlib.uri_validate import query
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.views import APIView

from django.db.models import Q

from .models import Cake, CakeLevel, Order, CakeShape, CakeTopping, CakeDecor, CakeBerry
from .serializers import CakeSerializer, CakeLevelSerializer, OrderSerializer, CakePriceRequestSerializer
from .permissions import IsOwnerOrReadOnly, CanUpdateCake, CanDeleteCake, CanUpdateCakeLevel, CanCreateCakeLevel, \
    CanCreateCakeShape, CanUpdateCakeShape, CanCreateCakeTopping, CanDeleteCakeLevel, CanDeleteCakeShape, \
    CanDeleteCakeTopping, CanUpdateCakeTopping, CanCreateCakeBerry, CanUpdateCakeBerry, CanDeleteCakeBerry, \
    CanUpdateOrder, CanDeleteOrder, CanCreateCakeDecor, CanUpdateCakeDecor, CanDeleteCakeDecor, IsOwner


class CalculateCakePriceApiView(APIView):
    def post(self, request, **kwargs):
        serializer = CakePriceRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cake_params = serializer.validated_data
            cake_price = 0
            level = CakeLevel.objects.get(id=cake_params['level_id'])
            cake_price += level.price
            shape = CakeShape.objects.get(id=cake_params['shape_id'])
            cake_price += shape.price
            topping = CakeTopping.objects.get(id=cake_params['topping_id'])
            cake_price += topping.price
            if cake_params.get('berry_id'):
                berry = CakeBerry.objects.get(id=cake_params['berry_id'])
                cake_price += berry.price
            if cake_params.get('decor_id'):
                decor = CakeDecor.objects.get(id=cake_params['decor_id'])
                cake_price += decor.price
            return Response(status=status.HTTP_200_OK, data={"price": cake_price})


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
            return [CanDeleteCake()]
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
            return [CanCreateCakeLevel()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsOwnerOrReadOnly(), CanUpdateCakeLevel()]
        elif self.action == 'destroy':
            return [CanDeleteCakeLevel()]
        else:
            return [permissions.IsAuthenticated()]

class CakeShapeViewSet(viewsets.ModelViewSet):
    queryset = CakeShape.objects.all()
    serializer_class = CakeLevelSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [CanCreateCakeShape()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsOwnerOrReadOnly(), CanUpdateCakeShape()]
        elif self.action == 'destroy':
            return [CanDeleteCakeShape()]
        else:
            return [permissions.IsAuthenticated()]


class CakeToppingViewSet(viewsets.ModelViewSet):
    queryset = CakeTopping.objects.all()
    serializer_class = CakeLevelSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [CanCreateCakeTopping()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsOwnerOrReadOnly(), CanUpdateCakeTopping()]
        elif self.action == 'destroy':
            return [CanDeleteCakeTopping()]
        else:
            return [permissions.IsAuthenticated()]


class CakeBerryViewSet(viewsets.ModelViewSet):
    queryset = CakeBerry.objects.all()
    serializer_class = CakeLevelSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [CanCreateCakeBerry()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsOwnerOrReadOnly(), CanUpdateCakeBerry()]
        elif self.action == 'destroy':
            return [CanDeleteCakeBerry()]
        else:
            return [permissions.IsAuthenticated()]


class CakeDecorViewSet(viewsets.ModelViewSet):
    queryset = CakeDecor.objects.all()
    serializer_class = CakeLevelSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [CanCreateCakeDecor()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsOwnerOrReadOnly(), CanUpdateCakeDecor()]
        elif self.action == 'destroy':
            return [CanDeleteCakeDecor()]
        else:
            return [permissions.IsAuthenticated()]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsOwner()]
        elif self.action == 'retrieve':
            return [IsOwner()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [CanUpdateOrder()]
        elif self.action == 'destroy':
            return [CanDeleteOrder()]
        else:
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Order.objects.none()
        if self.request.user.is_superuser:
            return self.queryset
        user = self.request.user
        return Order.objects.filter(customer=user)