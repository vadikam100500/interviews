from django.contrib import admin

from .models import Mailing, Message


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'text',
                    'tag_filter', 'code_filter', 'end_date')
    search_fields = ('text',)
    list_filter = ('tag_filter', 'code_filter', 'start_date')
    empty_value_display = '-пусто-'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('id', 'send_time', 'status',
                    'mailing', 'contact')
    search_fields = ('mailing__text',)
    list_filter = ('send_time', 'status',)
    empty_value_display = '-пусто-'
