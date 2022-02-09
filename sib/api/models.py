from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

User = get_user_model()


class Deal(models.Model):
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='deals',
                                 verbose_name='Логин покупателя')
    item = models.CharField(max_length=200, verbose_name='Наименование товара')
    total = models.PositiveBigIntegerField(verbose_name='Сумма сделки')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара,шт')
    # В date не используется auto_now_add, т.к.
    # при чтении из csv, будет проставляться дата операции чтения
    date = models.DateTimeField(default=now,
                                verbose_name='Дата и время регистрации сделки')

    class Meta:
        ordering = ('-date',)
        verbose_name = 'сделка'
        verbose_name_plural = 'сделки'

    def __str__(self):
        return (f'Покупка {self.customer.username} '
                f'камня {self.item} в количестве {self.quantity} '
                f'на сумму {self.total} от {self.date}')
