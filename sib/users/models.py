from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    spent_money = models.PositiveBigIntegerField(
        default=0, editable=True,
        verbose_name='Cумма принесенного дохода',
    )

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        ordering = ('-spent_money',)
        swappable = 'AUTH_USER_MODEL'
