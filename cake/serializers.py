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
        fields = '__all__'


class CakeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeLevel
        fields = '__all__'

class CakeShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeShape
        fields = '__all__'

class CakeToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeTopping
        fields = '__all__'

class CakeBerrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeBerry
        fields = '__all__'

class CakeDecorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeDecor
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

