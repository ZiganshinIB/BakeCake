from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from .models import Cake, CakeLevel, CakeShape, CakeTopping, CakeBerry, CakeDecor, Order


class ClientRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('name', 'phone_number', 'email', 'password')
        extra_kwargs = {
            'email': {'required': False}
        }


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
    class Meta:
        model = Order
        fields = [
            'customer',
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
        ]
        read_only_fields = ['registered_at']

