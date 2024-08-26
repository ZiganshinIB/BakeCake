from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from .models import Cake, CakeLevel, CakeShape, CakeTopping, CakeBerry, CakeDecor, Order, Client


class ClientRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('name', 'phone_number', 'email', 'password')
        extra_kwargs = {
            'email': {'required': False}
        }


class ClientSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class CakePriceRequestSerializer(serializers.Serializer):
    level_id = serializers.CharField(required=True)
    shape_id = serializers.CharField(required=True)
    topping_id = serializers.CharField(required=True)
    berry_id = serializers.CharField(required=False, allow_null=True)
    decor_id = serializers.CharField(required=False, allow_null=True)


class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = ['title', 'level', 'shape', 'topping', 'berry', 'decor', 'is_published', 'inscription', 'comment']

    def create(self, validated_data):
        validated_data['is_published'] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CakeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeLevel
        fields = ['level_count', 'price']


class CakeShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeShape
        fields = ['shape', 'price']


class CakeToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeTopping
        fields = ['cake_topping', 'price']


class CakeBerrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeBerry
        fields = ['cake_berry', 'price']


class CakeDecorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeDecor
        fields = ['cake_decor', 'price']


class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    cake = CakePriceRequestSerializer()
    inscription = serializers.CharField(required=False, allow_null=True)
    comment = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Order
        fields = [
            'client',
            'cake',
            'status',
            'status_pay',
            'registered_at',
            'called_at',
            'price',
            'address',
            'delivery_date',
            'delivered_at',
            'delivery_comments',
            'inscription',
            'comment'
        ]
        read_only_fields = ['registered_at']

