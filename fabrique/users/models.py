from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from pytz import all_timezones


class CustomUserManager(UserManager):

    def _create_user(self, username, email, password,
                     phone, tag, time_zone, **extra_fields):
        req_fields = {
            username: 'Введите никнейм',
            email: 'Введите почтовый адрес',
            password: 'Введите пароль',
            phone: 'Введите ваш телефон в формате 7ХХХХХХХХХХ',
            tag: 'Выберите вашу категорию',
            time_zone: 'Выберите часовой пояс в котором вы находитесь'
        }
        for field, message in req_fields.items():
            if not field:
                raise ValueError(message)
        email = self.normalize_email(email)
        globalusermodel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = globalusermodel.normalize_username(username)
        user = self.model(
            username=username, email=email, phone=phone,
            tag=tag, time_zone=time_zone, **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, phone,
                    tag, time_zone, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, phone,
                                 tag, time_zone, **extra_fields)

    def create_superuser(self, username, email, password, phone,
                         tag, time_zone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, phone,
                                 tag, time_zone, **extra_fields)


class ClientRole(models.TextChoices):
    FREE = 'Basic', _('Basic')
    ECONOM = 'Premium', _('Premium')
    NORM = 'Premium Pro', _('Premium Pro')


class CustomUser(AbstractUser):
    email = models.EmailField(_('Пользовательский email'), max_length=250,
                              unique=True)
    phone_regex = RegexValidator(regex=r"^7\d{10}$",
                                 message=('Ваш номер должен начинаться с 7 '
                                          'и содержать еще 10 цифр!'))
    phone = models.CharField(_('Номер телефона'), validators=[phone_regex],
                             max_length=11, unique=True)
    operator_сode = models.CharField(_('Код оператора'), max_length=3,
                                     editable=False, db_index=True)
    tag = models.CharField(_('Категория клиента'),
                           choices=ClientRole.choices, max_length=100,
                           default=ClientRole.FREE, db_index=True)
    time_zone = models.CharField(_('Часовой пояс'), max_length=100,
                                 choices=[(timezone, timezone)
                                          for timezone in all_timezones])

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', 'phone', 'operator_сode', 'tag', 'time_zone']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        self.operator_сode = self.phone[1:4]
        super().save(*args, **kwargs)
