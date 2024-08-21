from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneNumberAuthBackend(object):
    def authenticate(self, phone_number=None, pin=None):
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None
        if pin == user.pin:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
