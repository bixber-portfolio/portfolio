from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User


@admin.register(User)
class AdminUser(UserAdmin):
    readonly_fields = ('last_login_ip', 'last_login', 'date_joined')

    list_display = (
        'username',
        'first_name',
        'last_name',
        'role',
        'email',
        'phone_number',
        'last_login',
    )

    list_filter = (
        'role',
        'is_news_sub',
        'last_login',
        'date_joined',
    )

    fieldsets = (
        ('Данные аутентификации', {'fields': (
            'username',
            'email',
            'phone_number',
            'password',
        )}),
        ('Персональная информация', {'fields': (
            'first_name',
            'last_name',
            'patronymic',
        )}),
        ('Права доступа', {'fields': (
            'role',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        ('Дополнительные опции', {'fields': (
            'is_news_sub',
        )}),
        ('Данные об активности', {'fields': (
            'last_login_ip',
            'last_login',
            'date_joined',
        )}),
    )
    add_fieldsets = (
        ('Данные аутентификации', {'fields': (
            'username',
            'email',
            'password1',
            'password2',
        )}),
        ('Персональная информация', {'fields': (
            'first_name',
            'last_name',
        )}),
        ('Права доступа', {'fields': (
            'role',
            'is_active',
            'is_staff',
            'groups',
            'user_permissions',
        )}),
    )


admin.site.empty_value_display = '—'
