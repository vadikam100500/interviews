from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    spent_money = models.PositiveBigIntegerField(
        verbose_name='Cумма принесенного дохода'
    )
