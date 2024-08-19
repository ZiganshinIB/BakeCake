from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from .managers import ClientManager

class Client(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    # Имя пользователя
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    # Телефоный номер для входа
    phonenumber = PhoneNumberField(
        "Телефоный номер",
        unique=True,
        help_text="Телефоный номер должен быть русского формата 8XXXXXXXXXX",
        error_messages={
            'unique': "Телефон уже зарегистрирован",
        },
    )

    # Почта
    email = models.EmailField(_("email address"), blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = ClientManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['phonenumber']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return "{} {}".format(self.name, self.phonenumber)

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

