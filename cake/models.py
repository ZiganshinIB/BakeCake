from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from .managers import ClientManager


class CakeLevel(models.Model):
    level_count = models.IntegerField(
        verbose_name='Количество уровней',
        validators=[
            MinValueValidator(1)
        ]
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=7,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Уровень торта'
        verbose_name_plural = 'Уровни торта'

    def __str__(self):
        return f'{self.level_count}'


class CakeShape(models.Model):
    shape = models.CharField(
        max_length=50,
        verbose_name='Форма',
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=7,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Форма торта'
        verbose_name_plural = 'Формы торта'

    def __str__(self):
        return self.shape


class CakeTopping(models.Model):
    cake_topping = models.CharField(
        max_length=50,
        verbose_name='Топпинг',
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=7,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Топпинг'
        verbose_name_plural = 'Топпинги'

    def __str__(self):
        return self.cake_topping


class CakeBerry(models.Model):
    cake_berry = models.CharField(
        max_length=15,
        verbose_name='Ягоды',
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=7,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Ягода'
        verbose_name_plural = 'Ягоды'

    def __str__(self):
        return self.cake_berry


class CakeDecor(models.Model):
    cake_decor = models.CharField(
        max_length=15,
        verbose_name='Декор'
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=7,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Декор'
        verbose_name_plural = 'Декор'

    def __str__(self):
        return self.cake_decor


class Cake(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название торта',
        blank=True
    )
    level = models.ForeignKey(
        CakeLevel,
        verbose_name='Количество уровней торта',
        related_name='levels',
        on_delete=models.CASCADE
    )
    shape = models.ForeignKey(
        CakeShape,
        verbose_name='Форма торта',
        related_name='shapes',
        on_delete=models.CASCADE
    )
    topping = models.ForeignKey(
        CakeTopping,
        verbose_name='Топпинг',
        related_name='toppings',
        on_delete=models.CASCADE
    )
    berry = models.ForeignKey(
        CakeBerry,
        verbose_name='Ягоды',
        related_name='berries',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    decor = models.ForeignKey(
        CakeDecor,
        verbose_name='Декор',
        related_name='decors',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    is_published = models.BooleanField(
        verbose_name='Опубликован',
        default=False
    )
    inscription = models.CharField(
        max_length=200,
        verbose_name='Надпись на торте',
        blank=True
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True
    )
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Торт'
        verbose_name_plural = 'Торты'

    def __str__(self):
        return "{} уровень {}".format(self.title, self.level.level_count)


class Order(models.Model):
    STATUS = (
        ('new', 'Новый'),
        ('progress', 'В процессе'),
        ('delivered', 'Передан в доставку'),
        ('completed', 'Выполнен'),
        ('canceled', 'Отменен'),
    )
    STATUS_PAY = (
        ('y', 'Оплачен'),
        ('n', 'Не оплачен'),
    )

    customer = models.ForeignKey(
        'Client',
        verbose_name='Заказчик',
        related_name='orders',
        on_delete=models.CASCADE
    )
    cake = models.ForeignKey(
        Cake,
        verbose_name='Заказанный торт',
        related_name='orders',
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        max_length=20,
        verbose_name='Статус заказа',
        choices=STATUS,
        default='n'
    )
    status_pay = models.CharField(
        max_length=1,
        verbose_name='Статус оплаты',
        choices=STATUS_PAY,
        default='n'
    )
    registered_at = models.DateTimeField(
        'Время регистрации заказа',
        auto_now_add=True,
        db_index=True
    )
    called_at = models.DateTimeField(
        'Время звонка клиенту',
        blank=True,
        null=True,
        db_index=True
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=10,
        decimal_places=2
    )
    address = models.CharField(
        'Адрес доставки',
        max_length=200,
        blank=True,
    )
    delivery_date = models.DateTimeField(
        'Дата доставки',
        blank=True,
        null=True,
        db_index=True
    )
    delivered_at = models.DateTimeField(
        'Время доставки',
        blank=True,
        null=True,
        db_index=True
    )
    delivery_comments = models.TextField(
        verbose_name='Комментарий для курьера',
        blank=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-registered_at']

    def __str__(self):
        return f'{self.customer}: {self.registered_at}'


class Pay(models.Model):
    _TYPE = (
        ('tips', "Чаевые"),
        ('service', "Услуга"),
    )
    order_id = models.BigIntegerField(verbose_name="Номер записи", blank=True, null=True)
    operation_id = models.CharField(verbose_name="ID операции", max_length=255, unique=True)
    amount = models.DecimalField(verbose_name="Сумма", max_digits=10, decimal_places=2, blank=True, null=True)
    is_success = models.BooleanField(verbose_name="Успешно", blank=True, null=True)
    _type = models.CharField(verbose_name="Тип", max_length=255, choices=_TYPE, blank=True, null=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.operation_id}"


class Client(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    # Имя пользователя
    name = models.CharField(
        _('name'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        null=True,
        blank=True
    )
    # Телефоный номер для входа
    phone_number = PhoneNumberField(
        "Телефоный номер",
        unique=True,
        help_text="Телефоный номер должен быть русского формата 8XXXXXXXXXX",
        error_messages={
            'unique': "Телефон уже зарегистрирован",
        },
    )

    # Почта
    email = models.EmailField(_("email address"), blank=True)
    # pin
    pin = models.CharField(_("pin"), max_length=4, blank=True)

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
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return "{} {}".format(self.name, self.phone_number)

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"
