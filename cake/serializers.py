from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer


class ClientRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('name', 'phone_number', 'email', 'password')
        extra_kwargs = {
            'email': {'required': False}
        }
