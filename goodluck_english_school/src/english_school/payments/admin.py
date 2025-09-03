from django.contrib import admin

from .models import Wallet, WalletStatus, WalletTransaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'user',
        'balance',
        'status',
    )
    list_filter = (
        'status',
    )
    fieldsets = (
        ('Пользователь', {'fields': (
            'user',
        )}),
        ('Баланс', {'fields': (
            'balance',
        )}),
        ('Статус', {'fields': (
            'status',
        )}),
    )
    add_fieldsets = (
        ('Пользователь', {'fields': (
            'user',
        )}),
        ('Баланс', {'fields': (
            'balance',
        )}),
        ('Статус', {'fields': (
            'status',
        )}),
    )


@admin.register(WalletStatus)
class WalletStatusAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'title',
        'description',
    )
    list_filter = (
        'title',
    )
    fieldsets = (
        ('Идентификатор', {'fields': (
            'code',
        )}),
        ('Уникальное название', {'fields': (
            'title',
        )}),
        ('Описание', {'fields': (
            'description',
        )}),
    )
    add_fieldsets = fieldsets


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    pass
