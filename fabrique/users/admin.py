from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1',
                       'password2', 'phone',
                       'tag', 'time_zone', 'email'),
        }),
    )

    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('phone', 'tag', 'time_zone',)
        }),
    )

    list_display = ('username', 'email', 'tag', 'phone',
                    'operator_сode', 'time_zone', 'email', 'is_staff')
    list_filter = ('tag', 'operator_сode')
    search_fields = ('username', 'tag')


admin.site.unregister(Group)
