from django.contrib import admin

from .models import Deal


@admin.register(Deal)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'item',
                    'total', 'quantity', 'date')
    search_fields = ('customer__username', 'item',
                     'total', 'quantity', 'date')
    list_filter = ('item', 'date')
    empty_value_display = '-пусто-'
