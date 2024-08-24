from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from .models import Cake, CakeLevel, CakeShape, CakeTopping, CakeBerry, CakeDecor, Order


class ClientRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('name', 'phone_number', 'email', 'password')
        extra_kwargs = {
            'email': {'required': False}
        }


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
        cake = Cake.objects.create(
            title=validated_data['title'],
            level=CakeLevel.objects.get(id=validated_data['level'].id),
            shape=CakeShape.objects.get(id=validated_data['shape'].id),
            topping=CakeTopping.objects.get(id=validated_data['topping'].id),
            berry=CakeBerry.objects.get(id=validated_data['berry'].id),
            decor=CakeDecor.objects.get(id=validated_data['decor'].id),
            is_published=False
        )
        return cake

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

