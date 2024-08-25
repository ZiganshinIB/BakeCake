from oauthlib.uri_validate import query
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone

from django.db.models import Q

from .models import Cake, CakeLevel, Order, CakeShape, CakeTopping, CakeDecor, CakeBerry, Client
from .serializers import CakeSerializer, CakeLevelSerializer, OrderSerializer, CakePriceRequestSerializer
from .permissions import IsOwnerOrReadOnly, CanUpdateCake, CanDeleteCake, CanUpdateCakeLevel, CanCreateCakeLevel, \
    CanCreateCakeShape, CanUpdateCakeShape, CanCreateCakeTopping, CanDeleteCakeLevel, CanDeleteCakeShape, \
    CanDeleteCakeTopping, CanUpdateCakeTopping, CanCreateCakeBerry, CanUpdateCakeBerry, CanDeleteCakeBerry, \
    CanUpdateOrder, CanDeleteOrder, CanCreateCakeDecor, CanUpdateCakeDecor, CanDeleteCakeDecor, IsOwner


class OrderApiView(APIView):

    def post(self, request, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order_params = serializer.validated_data
            client = Client.objects.create(
                name=order_params['client']['name'],
                phone_number=order_params['client']['phone_number'],
                email=order_params['client']['email'],
                password=order_params['client']['password'],
            )
            if 'berry_id' in order_params['cake']:
                berry = CakeBerry.objects.get(id=order_params['cake']['berry_id'])
            else:
                berry = None
            if 'decor_id' in order_params['cake']:
                decor = CakeDecor.objects.get(id=order_params['cake']['decor_id'])
            else:
                decor = None
            if 'inscription' in order_params['cake']:
                inscription = order_params['cake']['inscription']
            else:
                inscription = " "
            if 'comment' in order_params['cake']:
                comment = order_params['cake']['comment']
            else:
                comment = " "
            cake = Cake.objects.create(
                title='Торт',
                level=CakeLevel.objects.get(id=order_params['cake']['level_id']),
                shape=CakeShape.objects.get(id=order_params['cake']['shape_id']),
                topping=CakeTopping.objects.get(id=order_params['cake']['topping_id']),
                berry=berry,
                decor=decor,
                is_published=False,
                inscription=inscription,
                comment=comment
            )
            if 'delivery_comments' in order_params:
                delivery_comments = order_params['delivery_comments']
            else:
                delivery_comments = " "
            order = Order.objects.create(
                customer=Client.objects.get(id=client.id),
                cake=Cake.objects.get(id=cake.id),
                price=order_params['price'],
                address=order_params['address'],
                delivery_date=order_params['delivery_date'],
                delivered_at=order_params['delivered_at'],
                delivery_comments=delivery_comments
            )
            return Response(status=status.HTTP_200_OK, data={"order": order.id})


class CakeApiView(APIView):

    def get(self, request, **kwargs):
        cake_detail = {'label': 'Без надписи'}
        params = request.query_params
        if 'level_id' in params:
            level = CakeLevel.objects.get(id=params['level_id'])
            cake_detail.update({'level': level.level_count})
        if 'shape_id' in params:
            shape = CakeShape.objects.get(id=params['shape_id'])
            cake_detail.update({'shape': shape.shape})
        if 'topping_id' in params:
            topping = CakeTopping.objects.get(id=params['topping_id'])
            cake_detail.update({'topping': topping.cake_topping})
        if 'berry_id' in params:
            berry = CakeBerry.objects.get(id=params['berry_id'])
            cake_detail.update({'berry': berry.cake_berry})
        if 'decor_id' in params:
            decor = CakeDecor.objects.get(id=params['decor_id'])
            cake_detail.update({'decor': decor.cake_decor})
        if 'label' in params:
            cake_detail['label'] = params['label']
        return Response(status=status.HTTP_200_OK, data=cake_detail)


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