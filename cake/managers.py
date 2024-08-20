from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class ClientManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, name, password, **extra_fields):
        if not phone_number:
            raise ValueError("Телефон не может быть пустым")
        if not name:
            raise ValueError("Имя не может быть пустым")
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(name=name, phone_number=phone_number, password=password, **extra_fields)
