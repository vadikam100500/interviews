from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.services import MailingManager
from users.models import ClientRole

User = get_user_model()

codes_list = [(f'{num}'.zfill(3), f'{num}'.zfill(3)) for num in range(1, 1000)]


class Mailing(models.Model):
    start_date = models.DateTimeField(_('Дата и время запуска рассылки'),
                                      null=False, blank=False)
    text = models.CharField(_('Текст сообщения'), max_length=100500)
    tag_filter = models.CharField(_('Фильтр рассылки по тэгам'),
                                  max_length=100, null=True, blank=True,
                                  choices=ClientRole.choices)
    code_filter = models.CharField(_('Фильтр рассылки по кодам оператора'),
                                   max_length=3, choices=codes_list,
                                   blank=True, null=True)
    end_date = models.DateTimeField(_('Дата и время окончания рассылки'),
                                    blank=True, null=True)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        constraints = [
            models.CheckConstraint(
                name='Начало рассылки должно быть раньше окончания',
                check=models.Q(start_date__lte=models.F('end_date'))
            )
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        manager = MailingManager(self.tag_filter, self.code_filter,
                                 self.start_date, self.end_date,
                                 self.text, self, Message)
        manager.start()

    def __str__(self):
        return f'Рассылка от {self.start_date} - {self.end_date}'


class Message(models.Model):
    STATUS_CHOICES = (
        ('S', 'send'),
        ('N', 'not send'),
    )
    send_time = models.DateTimeField(_('Дата и время создания (отправки)'),
                                     auto_now_add=True)
    status = models.CharField(_('Cтатус отправки'), max_length=1,
                              choices=STATUS_CHOICES)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE,
                                related_name='messages',
                                verbose_name='Рассылка')
    contact = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='messages',
                                verbose_name='Клиент')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'Сообщение отправлено {self.contact.username}-{self.send_time}'
